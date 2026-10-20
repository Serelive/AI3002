# Lab 1 / p02：Task 2 主体实施指南

英文对应文件：[p02_guide_main-eng.md](p02_guide_main-eng.md)。其中的代码片段是实施示例，并非完整训练脚本。

## 0. 范围、依据与当前状态

先读 `docs/instruction.pdf` 的 §2.1、§2.2、§3、附录 C.1，再读 `scr/model.py` 和 `scr/train23.py`。除特别说明外，本文路径相对于 `assignments/labs/lab1/`；终端命令在**课程仓库根目录**执行。步骤对应 [roadmap](../roadmap.md) 的 `p02-i00` 至 `p02-i07`。

目标：从**某一层**的 2,560 维表征预测 `[纬度, 经度]`。固定 LLM，仅训练线性探测模型；使用已提供的特征无需 GPU，也无需下载 LLM。暂不展开思考题 4–7、地图绘制或表征解释；层数和正则化的选择仍属于主体训练流程。

教师明确要求：选择 0–35 中的一层；导出 `float64` 的 `weights`，形状为 `(2, 2560)`，以及 `bias`，形状为 `(2,)`；第一行/项是纬度，第二行/项是经度；另行提交层号。最终权重可以由库训练得到，但 Task 1 仍要求手写支持 L1、L2 的梯度下降训练过程。

下文的基线、搜索网格与日志格式属于实施建议，并非新增评分要求。[课程仓库](https://github.com/ChangshuoShen/USTC-AI3002-26fall/) 的截止日期是 **2026 年 10 月 21 日**，已于 10 月 14 日核查；本地 `scr/README.md` 写的是 10 月 31 日。按 21 日安排，并核对班级通知。本次无法抓取上游实验子目录，因此具体任务要求依据本地 `instruction.pdf`。

10 月 14 日实际检查：六个 world 特征数组均为有限值 `float16`，形状符合要求；两个 CSV 均有四个预期列且无缺失值。当前 Python / NumPy / pandas 版本为 `3.14.4 / 2.5.3 / 3.0.6`。编写本指南时未执行 Task 2 训练，也未生成模型效果结果。

## 1. p02-i00：确认起点

先运行已有的线性回归检查，并查看训练接口：

```bash
.venv/bin/python assignments/labs/lab1/scr/p01_test_linear-regression.py
.venv/bin/python assignments/labs/lab1/scr/train23.py --help
```

当前 `fit()` 每次从零初始化，执行 `max_iter` 次更新，没有收敛日志或提前停止。默认 `lr=0.01`、`max_iter=10000`、`l1=l2=0`，这些设置尚未在 world 数据上验证。

`train23.py` 当前仅接受 `task`、`layer`、`output` 三个位置参数。其 world 分支已实现两个回归模型的组合与正确的导出布局，直接扩展即可；同时保持 Task 3 的 truth 分支可用。

**完成标准：**能够沿着 `load_split → fit → predict → MSE → np.savez` 解释数据流与形状。小样例测试通过不等于真实数据训练稳定。

## 2. p02-i01：检查输入约定

输入位于 `scr/datasets/world/`：

| 文件 | 形状或内容 |
| --- | --- |
| `train.csv` | 500 行；`sentence, country, latitude, longitude` |
| `valid.csv` | 130 行；列名相同 |
| `train.layer{11,23,35}.npy` | 每份 `(500, 2560)`，`float16` |
| `valid.layer{11,23,35}.npy` | 每份 `(130, 2560)`，`float16` |

CSV 第 i 行对应特征数组第 i 行。不能单独排序、筛选或打乱其中一份文件；行数相同只能验证数量，不能证明语义对齐，因此应保留原始顺序。`country` 和 `sentence` 是元数据，不作为额外输入特征。坐标单位是度，北纬、东经为正。

复用 `load_split("world", "train", layer)` 及相应验证集调用。它已将特征和标签转为 `float64`。训练前检查形状、类型、有限性以及纬度/经度取值范围。使用已提供数据时，将层号限制为 `11, 23, 35`；缺文件时明确报错。

训练集用于拟合参数，验证集用于选择设置，隐藏测试集不参与调参。初始流程不合并训练集与验证集。保持原始输入不变。

## 3. p02-i02：把双输出公式对应到代码

对于 `(N, D)` 的 `X` 与 `(N, 2)` 的 `Y`，分别拟合两个目标：

```text
L_k = mean((X @ w_k + b_k - Y[:, k])**2)
      + l1 * sum(abs(w_k)) + l2 * sum(w_k**2),  k = 0, 1
```

每个 `w_k` 为 `(D,)`，`b_k` 为标量，偏置不正则化。平方误差按输出坐标可分离，因此可独立训练两个模型。

```python
latitude_targets = train_y[:, 0]       # (N,)，不要写成 (N, 1)
longitude_targets = train_y[:, 1]
prediction = np.column_stack((lat_pred, lon_pred))         # (N, 2)
W = np.stack((lat_model.weights, lon_model.weights))       # (2, D)
b = np.array((lat_model.bias, lon_model.bias))             # (2,)
prediction_from_parameters = valid_x @ W.T + b             # (N, 2)
```

`column_stack` 把两个预测向量作为列；`stack` 给两个权重向量增加行轴；`W.T` 将 `(2, D)` 转为 `(D, 2)`；广播把两个偏置加到每行。尤其注意：`(N, 1)` 的标签减去 `(N,)` 的预测可能广播成 `(N, N)`，不会自动替你发现错误。

## 4. p02-i03：先建立稳定、可观察的基线

先为 `train23.py` 增加 `--lr`、`--max-iter`、`--l1`、`--l2`，传给两个坐标模型并记录配置。**这些选项目前尚不存在。**拒绝非正学习率、非正迭代次数以及负正则化系数。初始使用原始 `float64` 特征、第 11 层、`l1=l2=0`。

在 `fit()` 中加入可选的周期性训练目标日志，以及损失、梯度、参数的有限性检查；遇到无效值应停止，不能导出坏权重。记录实际迭代数和停止原因。验证集不得参与梯度计算。先短跑观察损失，再增加迭代预算，不要用未经检查的学习率直接启动大规模搜索。

当 `l1=0` 时，可以从以下保守学习率开始：

```python
A = np.column_stack((train_x, np.ones(len(train_x))))
L_bound = 2 * np.sum(A * A) / len(A) + 2 * l2
lr = 0.9 / L_bound
```

Hessian 为 `2 A.T @ A / N` 加上 L2 的对角项，其中偏置不受罚。矩阵 Frobenius 范数的平方是谱范数平方的上界，因此上述表达式给出曲率上界，但可能使学习率过小、训练较慢。每个配置只计算一次；必要时再用更紧的谱范数界或经过检查的较大学习率。这一光滑目标的收敛论证**不适用于 L1**；固定步长的次梯度法可能在零点附近振荡。

当前已有接口如下，仅作参考：

```bash
.venv/bin/python assignments/labs/lab1/scr/train23.py world 11 --output_dir assignments/labs/lab1/output/p02/baseline-layer11
```

该命令使用上面的未验证默认值。新增选项后，应显式传入计算得到的学习率和选择的迭代上限。不要将这条参考命令描述为已验证稳定的基线或已获得的实验结果。

**完成标准：**完整数据训练结束，预测与权重均有限，配置可复现；光滑目标训练损失下降。

## 5. p02-i04：评价基线并保存证据

分别计算训练集与验证集误差：

```python
mse_by_coordinate = np.mean((prediction - targets)**2, axis=0)  # (2,)
mse = float(mse_by_coordinate.mean())
rmse_by_coordinate = np.sqrt(mse_by_coordinate)
```

现有脚本的 MSE 同时平均样本和坐标，即 `(纬度 MSE + 经度 MSE) / 2`，单位为平方度；RMSE 单位为度。它们不是公里距离。讲义未给出隐藏测试的精确评分公式，这里的 MSE 是所提供脚本采用的本地比较指标。不要悄悄裁剪预测或对经度取模，应评价实际导出的线性映射。

增加一个仅用训练标签估计的常数预测基线：

```python
mean_coordinate = train_y.mean(axis=0)
baseline_prediction = np.broadcast_to(mean_coordinate, valid_y.shape)
```

它用于合理性检查，不是人为设定的及格线。若模型提升很小，先排查收敛、坐标顺序、特征与标签对齐，再扩大实验。

开始实验时创建 `output/p02/`，每次运行保存：

- `metrics.csv` 中的一行：运行编号、层号、L1/L2、学习率、最大及实际迭代次数、停止原因、训练/验证 MSE、各坐标误差、耗时。
- `config.json` 或等价记录：完整命令、预处理、依赖版本、初始化方式、代码版本；若引入随机性，再记录种子。
- 权重 `.npz`、训练日志，以及按原顺序保存的验证集预测，含行号、真实纬度/经度、预测纬度/经度。

零初始化的全批量训练不涉及随机采样，应如实记录，不要声称使用了无效的种子。若加入打乱或随机算法，可固定种子如 `42` 并记录。不同运行不能互相覆盖。

## 6. p02-i05：在有限预算内选择层数和正则化

基线稳定后，按同一评价流程比较第 11、23、35 层。建议初始 L2 网格为 `{0, 1e-4, 1e-2, 1, 100}`，固定 `l1=0`。这只是起点，合适范围依赖特征尺度。每层、每个 L2 配置重新计算稳定学习率并检查收敛，避免把优化过慢误判为模型较差。若最优点在边界，可适度扩展一次。初始让两个坐标模型共用正则化设置。

对有限且充分优化的运行，按验证 MSE 排序，同时查看两个坐标各自的误差。这里 `D=2560 > N=500`，训练误差低不能单独作为选择依据。搜索前记录平局规则，例如验证 MSE 在数值精度内相同时优先较大的 L2。控制反复调参次数；用于选模型后的验证误差不再是无偏的测试误差估计。

小规模 L1 比较对于本主体流程是可选的；Task 1 实现两种正则化的要求仍然有效。§2.2 允许使用库训练最终权重，但建立手写模型基线不必依赖库模型。

## 7. 可选预处理：保证导出参数可直接用于原始特征

仅在确有优化问题时加入标准化。均值 `mu` 和标准差 `s` **仅由训练集计算**，将零标准差替换为 1，对验证集使用同一变换。缩放会改变正则化的含义，因此须单独标记这些运行。

最终参数必须直接作用于原始特征，不能依赖额外的 scaler。若 `Z=(X-mu)/s`，在标准化空间训练的参数为 `W_z, b_z`，则：

```python
W_raw = W_z / s[None, :]
b_raw = b_z - W_raw @ mu
np.testing.assert_allclose(
    valid_x @ W_raw.T + b_raw,
    ((valid_x - mu) / s) @ W_z.T + b_z,
    rtol=1e-9, atol=1e-8,
)
```

容差是建议的 `float64` 检查设置，不是教师要求。初始流程不缩放标签，保持单位为度；标签缩放还需要额外逆变换。不能把标准化空间中的权重当作原始空间权重提交。

## 8. p02-i06–i07：重新加载、核对并冻结候选

保存后，在新进程中用 `allow_pickle=False` 重新加载：

```python
with np.load(output_path, allow_pickle=False) as archive:
    assert set(archive.files) == {"weights", "bias"}
    W, b = archive["weights"], archive["bias"]
assert W.shape == (2, 2560) and b.shape == (2,)
assert W.dtype == np.float64 and b.dtype == np.float64
assert np.isfinite(W).all() and np.isfinite(b).all()
reloaded_prediction = valid_x @ W.T + b
assert np.isfinite(reloaded_prediction).all()
np.testing.assert_allclose(reloaded_prediction, prediction,
                           rtol=1e-9, atol=1e-8)
```

其中 `prediction` 是同一次运行导出前保存的验证预测，`valid_x` 必须来自该运行的层。重新计算 MSE；逐项预测一致比仅验证 MSE 一致更可靠。还要对照训练模型确认第 0 行是纬度、第 1 行是经度。

将选定候选保存为 `output/p02/world.npz`，层号写入 `output/p02/world-layer.txt`，配置与指标放在旁边。这些是本地命名约定，不是教师规定的文件名。先在新进程中复现，再有意识地将最终文件复制到 `submission/`。更新实验 README，写明完整命令、层数、指标和限制。

不能宣称 Task 2 报告已完成：思考题 4–7 仍待处理，Task 3 与全实验打包也尚未完成。验证集预测改善只说明在该数据划分上具有预测价值，不能单独证明 LLM 如何使用地理知识。

## 排错顺序与完成标准

| 症状 | 优先检查 |
| --- | --- |
| 缺输入文件 | `docs/INPUTS.md` 和输入来源；不能伪造数据 |
| 形状错误 | `(N,)`、`(N, 2)`、`(2, D)`、`(2,)` 及坐标顺序 |
| NaN/inf 或光滑损失上升 | 是否转为 `float64`，学习率是否过大 |
| 损失几乎不变 | 梯度量级、学习率、实际更新次数 |
| 训练误差低、验证误差高 | 先核实收敛，再考虑 L2 和层数 |
| L1 振荡 | 步长与目标轨迹，不要直接延长运行 |
| 重新加载结果不一致 | 层号、转置、偏置、行序、预处理折回 |

主体完成标准：预测有限且可复现；配置经验证集选择并记录；原始特征上的 `.npz` 推理通过检查；所选层号有明确记录。
