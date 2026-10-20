# p02 minimal checklist: Task 2 main work

This replaces the earlier eleven-step engineering checklist. Follow the local `docs/instruction.pdf` §2.2 for Task 2 requirements and §3 for the full-lab submission. **Prioritize a working coordinate predictor and correctly formatted weights.** Spend a limited amount of time improving validation performance, then move on: the handout explicitly gives Task 3 more model-performance weight than Task 2.

Paths below are relative to `assignments/labs/lab1/`. This checklist covers the main implementation only; the report questions remain separate work. Finishing this checklist does not finish the entire lab.

## Already done — do not repeat

- [x] `p02-i00`: linear-regression checks and CLI-help check passed.
- [x] `p02-i01`: the six supplied world input pairs passed the data checks.

Keep the existing scripts and evidence. No additional input-checking infrastructure is needed before training.

## 1. Highest priority: train one usable coordinate model (`p02-i03`)

- [ ] Use one supplied layer, starting with 11. Fit latitude and longitude from its **training** features, and predict both coordinates on its **validation** features.

**Use what exists:** `scr/train23.py` already loads the data, fits two `LinearRegressionModel` instances, prints validation MSE, and saves weights. Its options are `--output_dir`, `--lr`, `--l1`, `--l2`, and `--max_iter`. Start with `l1=0`; choose an explicit L2 value rather than accidentally relying on the current defaults. Reuse `scr/p02_scaffold.ipynb` for exploration if convenient.

**Done when:** one run produces finite `(130, 2)` validation predictions, a finite validation MSE, and a saved `.npz`. Column 0 is latitude; column 1 is longitude. No separate toy-test script, logging system, or CLI-hardening task is required first.

If training produces NaN/infinity or clearly diverges, reduce the learning rate and rerun. If optimization remains a time sink, use a library linear regressor, such as Ridge, for the final Task 2 weights: **§2.2 explicitly permits this.** Keep the handwritten Task 1 implementation, which is still required by §2.1. If a new runner is needed, name it `scr/p02_train_world.py` and keep it small. Use raw features initially to avoid adding preprocessing/export work.

## 2. Next priority: make a small validation comparison (`p02-i05`)

- [ ] Compare a few layer/regularization choices and keep the best observed validation result.

The handout suggests different layers and regularization to improve generalization; it does **not** prescribe a grid size, number of runs, convergence tolerance, or minimum score. A short practical route is:

1. Compare layers **11, 23, 35** with one working regularization setting.
2. On the best observed layer, try **one weaker and one stronger** regularization setting if time permits.
3. Choose the run with the lowest validation MSE among those actually tried. Do not choose by training error or tune on the hidden test set.

This roughly five-run plan is a time-saving suggestion, not a requirement or guarantee of the global best model. Stop after this small comparison if results are usable; skip further tuning when other lab deliverables need the time. Fix a visibly broken training run before comparing its score.

**Keep only a small record:** layer, estimator, regularization setting, validation MSE, and the command or settings needed to rerun the selected model. For handwritten training, include learning rate and iteration count. For a library model, record the library parameter name (for example `alpha`); do not assume it has the same normalization as the handwritten `l2`.

**Done when:** the selected layer/settings and actual comparison scores are recorded in the lab README or a short table in `docs/p02/`. A notebook table is sufficient during exploration. No mandatory JSON schema, automated search script, training histories, or repeated iteration-budget experiments are needed.

## 3. Essential before finishing: save the required artifact (`p02-i06`)

- [ ] Save the selected model with the exact interface required by §2.2:

| Item | Required format |
| --- | --- |
| `weights` in one `.npz` | `np.float64`, shape `(2, 2560)`; latitude row first, longitude second |
| `bias` in that `.npz` | `np.float64`, shape `(2,)`; same coordinate order |
| Selected layer | One integer in `[0, 35]`; use 11, 23, or 35 with the supplied features |

**Quick check:** load the saved archive once with `allow_pickle=False`; inspect the shapes, dtypes, coordinate order, and finite values. Compute `valid_x @ weights.T + bias` using the chosen layer and confirm it matches the selected model's validation predictions with `np.allclose`. This can be a notebook cell; no dedicated export-checking tool is needed.

If preprocessing was used, fold it into the exported weights and bias so this raw-feature prediction works. Otherwise use the existing export directly.

**Done when:** the archive passes that check, and the layer is recorded alongside it. A local convention is `output/p02/world.npz` plus `output/p02/world-layer.txt`; these filenames are not mandated by the handout. Preserve the selected run when experimenting further. Select the files for `submission/` when preparing the full lab submission; no upload is implied.

## Stop here for the main implementation

Record the selected model's runnable command and validation MSE in the lab README. Ensure the code used for the model is retained for submission and demonstration. A long evidence package is unnecessary. For a brief check, provide the step identifier; the reviewer can inspect the local code and outputs directly.

**Deferred unless an actual problem calls for them:** new test scripts, detailed optimizer histories, invalid-argument tests, overwrite guards, standardized experiment directories, large grids, convergence studies, extra feature extraction, and preprocessing. These are possible refinements, not prerequisites for this checklist.

The earlier detailed guides remain optional technical references. Their old workflow and CLI examples are not the current execution plan. Historical increments `p02-i02`, `p02-i03a/b/c`, `p02-i04`, and `p02-i07` are no longer separate gates; their useful parts are covered by the three priorities above. Completed work remains valid, and Git retains the previous checklist.
