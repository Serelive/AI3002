"""Train the coordinate or truth probe and save its parameters."""


from pathlib import Path

import numpy as np
import pandas as pd

from model import LinearRegressionModel, LogisticRegressionModel
import argparse

# 加载 task 任务的 train/valid 数据集，特征取自 layer 层
def load_split(
    task: str,
    split: str,
    layer: int
) -> tuple[np.ndarray, np.ndarray]:

    # 在 Python 中，Path(___) 表示当前脚本文件的路径
    data_dir = Path(__file__).parent / "datasets" / task

    features = np.load(data_dir / f"{split}.layer{layer}.npy", allow_pickle=False)
    labels = pd.read_csv(data_dir / f"{split}.csv")
    if task == "world":
        targets = labels[["latitude", "longitude"]].to_numpy(dtype=np.float64)
        # 形状为 (N, 2)
    else:
        targets = labels["label"].to_numpy(dtype=np.float64)
        # 形状为 (N,)
    if len(features) != len(targets):
        raise ValueError("The feature and label files have different row counts")

    return features.astype(np.float64), targets

def fit_standardizers(
    features: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0)
    std = np.where(std == 0, 1, std)
    return mean, std

def transform_features(
    features: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray
) -> np.ndarray:
    return (features - mean) / std

def reverse_weights_bias(
    model: LinearRegressionModel | LogisticRegressionModel,
    mean: np.ndarray,
    std: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    weights_original = model.weights / std
    bias_original = model.bias - mean @ weights_original
    return weights_original, bias_original

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("world", "truth"))
    parser.add_argument("layer", type=int)
    # 你可以在此处加入更多的命令行参数，例如学习率、训练轮数等
    parser.add_argument("--output_dir",
                        type=Path,
                        help="Path to the output folder",
                        )
    parser.add_argument("--lr", type = float, default=0.01)
    parser.add_argument("--l1", type = float, default = 0.01)
    parser.add_argument("--l2", type = float, default = 0.01)
    parser.add_argument("--max_iter", type = int, default = 10000)
    return parser

def main(args) -> float:
    if (not np.isfinite([args.lr, args.l1, args.l2]).all()
            or args.lr <= 0 or args.l1 < 0 or args.l2 < 0 or args.max_iter <= 0):
        raise ValueError("Require finite lr > 0, l1/l2 >= 0, and max_iter > 0")

    if args.output_dir is None:
        args.output_dir = Path(__file__).parent / "output" / args.task

    output = args.output_dir / f"{args.task}_layer{args.layer}.npz"
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite {output}; choose a new output_dir")

    # 加载数据
    train_x, train_y = load_split(args.task, "train", args.layer)
    valid_x, valid_y = load_split(args.task, "valid", args.layer)

    # 获取标准化参数
    train_x_mean, train_x_std = fit_standardizers(train_x)

    # 标准化
    standardized_train_x = transform_features(train_x, train_x_mean, train_x_std)
    standardized_valid_x = transform_features(valid_x, train_x_mean, train_x_std)

    if args.task == "world":
        # 纬度和经度各训练一个一维线性回归模型。
        latitude_targets = train_y[:, 0]
        longitude_targets = train_y[:, 1]

        # 初始化模型
        latitude_model = LinearRegressionModel(
            n_features=standardized_train_x.shape[1],
            l1=args.l1,
            l2=args.l2,
            lr=args.lr,
            max_iter=args.max_iter,
        )
        longitude_model = LinearRegressionModel(
            n_features=standardized_train_x.shape[1],
            l1=args.l1,
            l2=args.l2,
            lr=args.lr,
            max_iter=args.max_iter,
        )

        # 训练
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            latitude_model.fit(standardized_train_x, latitude_targets)
            longitude_model.fit(standardized_train_x, longitude_targets)

        # 预测
        latitude_predictions = latitude_model.predict(standardized_valid_x)
        longitude_predictions = longitude_model.predict(standardized_valid_x)
        prediction = np.column_stack((latitude_predictions, longitude_predictions))

        # 逆变换权重
        latitude_weights_original, latitude_bias_original = reverse_weights_bias(latitude_model, train_x_mean, train_x_std)
        longitude_weights_original, longitude_bias_original = reverse_weights_bias(longitude_model, train_x_mean, train_x_std)

        # 合并权重
        weights_original = np.stack((latitude_weights_original, longitude_weights_original))
        bias_original = np.array((latitude_bias_original, longitude_bias_original))

    else:
        # 初始化模型
        model = LogisticRegressionModel(
            n_features=train_x.shape[1],
            l1=args.l1,
            l2=args.l2,
            lr=args.lr,
            max_iter=args.max_iter,
        )

        # 训练模型
        model.fit(train_x, train_y)

        # 测试
        prediction = model.predict(valid_x)

        # 逆变换权重
        weights_original, bias_original = reverse_weights_bias(model, train_x_mean, train_x_std)

    if prediction.shape != valid_y.shape:
        raise ValueError(f"Expected predictions with shape {valid_y.shape}")

    if not all(np.isfinite(value).all() for value in
               (prediction, weights_original, bias_original)):
        raise FloatingPointError("Non-finite predictions or parameters; no weights saved")

    if args.task == "world":
        with np.errstate(over="raise", invalid="raise"):
            mse = float(np.mean((prediction - valid_y) ** 2))
        print(f"Validation MSE: {mse:.4f}")
    else:
        accuracy = np.mean((prediction >= 0.5) == valid_y)
        print(f"Validation accuracy: {accuracy:.4f}")

    # 创造输出目录（如果不存在的话）
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"{args.task}_layer{args.layer}.npz"

    # 输出文件的名称被 output 参数指定，文件格式为 .npz
    np.savez(
        output,
        weights=np.asarray(weights_original, dtype=np.float64),
        bias=np.asarray(bias_original, dtype=np.float64),
    )
    print(f"Saved {output} (layer {args.layer})")

    if args.task == "world":
        return mse
    else:
        return accuracy


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
