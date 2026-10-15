# p02 checklist: Task 2 main implementation

Use this checklist to submit **one small increment for review at a time**. This document covers coordinate prediction only; it contains no Task 2 report-question assignments. All boxes start unchecked: existing code may satisfy some items, but completion requires the evidence specified below.

Paths are relative to `../..`, except shell commands, which run from the **course repository root** using `.venv/bin/python`. Source requirements: `docs/instruction.pdf` §2.2 and Appendix C.1. The check thresholds, filenames, and experiment budget below are local workflow choices, not instructor grading rules.

## How to submit a step

For each numbered step, send its ID, changed code paths, exact command, and evidence-file paths. For example:

```text
[p02-i01][check]
Step 2 ready.
Code: main/check_world.py
Command: .venv/bin/python assignments/labs/lab1/main/check_world.py
Evidence: output/p02/input-check.txt
Please evaluate the Step 2 acceptance criteria.
```

Mark a box complete only after every acceptance criterion passes. If one fails, submit the failure output and leave the box unchecked. Here, “submit” means request local review, not upload to the course platform. Keep generated evidence in `output/p02/`; keep runnable scripts in `main/`. No testing framework or per-increment source directories are needed.

## Current starting point (inspected October 15, 2026)

- `main/train23.py` already accepts `task`, `layer`, `--output_dir`, `--lr`, `--l1`, `--l2`, and `--max_iter`. Use underscores exactly as shown.
- Both world models already receive the CLI training settings. Current CLI defaults are `lr=0.01`, `l1=l2=0.01`, `max_iter=10000`. Explicitly override both penalties for an unregularized baseline.
- Exports currently use `<output_dir>/world_layer<layer>.npz`. Reusing a directory with the same layer overwrites the previous file.
- `LinearRegressionModel.fit()` resets to zero and runs a fixed number of updates. It currently has no loss history or non-finite-value guard.
- `main/p02_scaffold.ipynb` exists and has local edits. It can support exploration, but the final run must work without notebook state. Its current paths depend on the notebook working directory; do not assume it can run from any directory.

The older bilingual guides provide equation explanations. For CLI spelling and the order of implementation work, follow this checklist; their original CLI examples predate the current code.

## Step 1 — Save the starting checks (`p02-i00`)

- [x] **Do:** Run these commands and save their combined output and exit status in `output/p02/start-check.txt` (create the output directory first):

```bash
.venv/bin/python assignments/labs/lab1/main/p01_test_linear-regression.py
.venv/bin/python assignments/labs/lab1/main/train23.py --help
```

**Hand in:** `start-check.txt`; no code change is required if both commands pass.

**Pass:** the regression script reports all three tests passing; both processes exit with status 0; help lists all five options above. If a regression fails, fix it before training on world data. Do not interpret these toy tests as a full-data performance result.

**Verified October 15, 2026:** all three regression tests passed; CLI help listed all five options; both exit statuses were 0. Evidence: `output/p02/start-check.txt`. The command above uses the renamed regression-test file.

## Step 2 — Write a six-file input check (`p02-i01`)

- [ ] **Do:** Create `main/check_world.py`. Import `load_split` from `train23`, loop over layers `(11, 23, 35)` and splits `("train", "valid")`, and assert the following for each loaded pair:

| Property | Train | Validation |
| --- | --- | --- |
| `X.shape` | `(500, 2560)` | `(130, 2560)` |
| `Y.shape` | `(500, 2)` | `(130, 2)` |
| Loaded `X.dtype`, `Y.dtype` | Both `float64` | Both `float64` |
| Finite values | Every element of X and Y | Every element of X and Y |
| Target bounds | Latitude in `[-90, 90]`; longitude in `[-180, 180]` | Same |

Read each CSV in its original order and assert that `Y[:, 0]` equals its `latitude` column and `Y[:, 1]` equals its `longitude` column. Assert that all layers of a split load the same targets. Print one result line per split/layer and finish with `PASS: 6 input pairs` only after all assertions succeed.

**Hand in:** `main/check_world.py`, its exact invocation, and `output/p02/input-check.txt`.

**Pass:** six result lines, the final PASS line, and exit status 0. No sorting, filtering, or mutation of input files. These checks establish the loader's contract; they cannot independently prove semantic alignment of the supplied feature rows.

## Step 3 — Prove the two-output layout on a tiny example (`p02-i02`)

- [ ] **Do:** Create `main/check_world_model.py` using the real `LinearRegressionModel`. Use:

```python
X = np.array([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
Y = np.column_stack((2 * X[:, 0] + 3, -4 * X[:, 1] + 5))
```

Train separate latitude and longitude models with `l1=l2=0`, `lr=0.1`, and `max_iter=200`. Form `P` using `np.column_stack`, `W` using `np.stack`, and `b` in latitude/longitude order, as in the world branch.

**Hand in:** the script and its console output in `output/p02/two-output-check.txt`.

**Pass:** `P.shape == (4, 2)`, `W.shape == (2, 2)`, `b.shape == (2,)`; all of these comparisons pass with `rtol=0, atol=1e-8`:

```python
np.testing.assert_allclose(P, Y, rtol=0, atol=1e-8)
np.testing.assert_allclose(W, [[2., 0.], [0., -4.]], rtol=0, atol=1e-8)
np.testing.assert_allclose(b, [3., 5.], rtol=0, atol=1e-8)
np.testing.assert_allclose(X @ W.T + b, P, rtol=0, atol=1e-8)
```

## Step 4 — Reject invalid settings and prevent overwritten runs (`p02-i03a`)

- [ ] **Do:** Extend `train23.py` without renaming the existing options. Reject non-finite or nonpositive `lr`, nonpositive `max_iter`, and non-finite or negative `l1/l2`. For the supplied world-data workflow, reject layers outside `(11, 23, 35)` with a useful message. Before training, refuse to overwrite the target `.npz`; use a fresh run directory for each experiment.

**Hand in:** the diff plus `output/p02/cli-check.txt`, containing commands, messages, and exit statuses for `--lr 0`, `--lr nan`, `--l1 -1`, `--l2 inf`, `--max_iter 0`, and `world 12`. Also demonstrate the existing-output guard with a temporary dummy output file under `output/p02/`; record its hash before and after.

**Pass:** each invalid invocation exits nonzero before training and identifies the offending setting; no new weight file is produced. The overwrite attempt exits nonzero and leaves the dummy file unchanged. `--help` still succeeds. Do not silently change the truth branch's behavior while making world-specific changes.

## Step 5 — Record the objective and stop on invalid numbers (`p02-i03b`)

- [ ] **Do:** Add training history to `LinearRegressionModel.fit()`. Record iteration 0, every 100 completed updates, and the final update, without duplicate rows. Each entry contains iteration, unregularized training MSE, and total objective:

```python
mse = np.mean((X @ w + b - y) ** 2)
objective = mse + l1 * np.abs(w).sum() + l2 * (w ** 2).sum()
```

Record `n_iter_` and a stopping reason (the existing fixed-loop behavior may use `max_iter`). Raise an error on non-finite gradients, parameters, or logged losses. Reject non-finite input arrays before the loop. In `train23.py`, write each coordinate's history to the run directory and do not export parameters after an error.

**Hand in:** the code diff; the Step 3 check rerun; a tiny deliberately non-finite input example that raises an error; a history generated with 201 updates.

**Pass:** all earlier regression checks still pass; the 201-update history has exactly iterations `[0, 100, 200, 201]`; its last objective equals an independent calculation from the final parameters within `rtol=1e-9, atol=1e-8`. An unregularized run has objective equal to MSE. Invalid input raises an error rather than producing an artifact. Do not require monotonic decrease for L1 subgradient descent.

## Step 6 — Run a stable layer-11 baseline (`p02-i03c`)

- [ ] **Do:** Using layer-11 **training** features in float64, compute and print a conservative learning rate for `l1=l2=0`:

```python
A = np.column_stack((train_x, np.ones(len(train_x))))
L_bound = 2 * np.sum(A * A) / len(A) + 2 * l2
lr = 0.9 / L_bound
```

Run 200 updates in a fresh directory; if the checks below pass, run 2,000 updates from zero in another directory. Insert the computed numeric rate in the command; `RATE` below is a placeholder, not a literal argument:

```bash
.venv/bin/python assignments/labs/lab1/main/train23.py world 11 \
  --output_dir assignments/labs/lab1/output/p02/baseline-l11-2000 \
  --lr RATE --l1 0 --l2 0 --max_iter 2000
```

**Hand in:** the calculation code or notebook cell, its printed rate, both exact commands, histories, and the 2,000-update `.npz`.

**Pass:** both runs finish; parameters and predictions are finite; each coordinate's final training objective is lower than its initial objective. For consecutive logged objectives, require `next <= previous + 1e-10 * max(1, abs(previous))`. This verifies stable progress, not convergence or acceptable predictive performance. The Frobenius-norm bound can produce a very small rate; investigate optimization speed before launching the search.

## Step 7 — Save metrics, predictions, and configuration (`p02-i04`)

- [ ] **Do:** Extend the runner to write these files in every successful run directory:

| File | Required contents |
| --- | --- |
| `config.json` | Task, layer, lr, l1, l2, max_iter, actual iterations for each model, stopping reasons, preprocessing (`none` initially), zero initialization, full command, Python/NumPy/pandas versions, code revision and whether code was uncommitted |
| `metrics.json` | Train and validation overall MSE, latitude MSE, longitude MSE; validation MSE of the training-mean predictor; training elapsed seconds |
| `valid_predictions.csv` | `row_index`, `true_latitude`, `true_longitude`, `pred_latitude`, `pred_longitude`, in original order |
| `latitude_history.csv`, `longitude_history.csv` | Step 5 history fields |
| `world_layer11.npz` (layer-dependent name) | Existing export |

Use `mean_coordinate = train_y.mean(axis=0)` for the constant predictor; never fit it using validation labels. Overall MSE is `np.mean((P-Y)**2)`, the mean of the two coordinate MSEs, in squared degrees. Do not clip or wrap predictions. Full-batch zero initialization requires no random seed; record `seed: null` unless randomness is actually introduced.

**Hand in:** the code diff and one new complete baseline run directory, using the same settings as Step 6.

**Pass:** all files exist; JSON parses; the prediction CSV has 130 rows with `row_index` exactly `0..129`; every numeric metric/prediction is finite; elapsed time is nonnegative. Recompute validation MSE from the CSV and compare with the saved value using `rtol=1e-9, atol=1e-8`. Overall MSE equals the average of coordinate MSEs. Report whether the model beats the constant baseline; no invented score threshold determines this step's acceptance.

## Step 8 — Run a fixed, small selection experiment (`p02-i05a`)

- [ ] **Do:** Before running, write `output/p02/search-plan.json` with layers `[11, 23, 35]`, L2 values `[0, 0.0001, 0.01, 1, 100]`, `l1=0`, no preprocessing, and one common iteration budget initially set to `2000`. Recompute the Step 6 rate for each layer/L2 combination. Use a distinct directory for each of the 15 configurations. A simple loop script in `main/` is sufficient.

Aggregate results into `output/p02/search.csv`: run directory, layer, l2, lr, iteration budget, train/validation overall and coordinate MSEs, elapsed seconds, success/failure, and failure reason. Do not substitute a score for failed runs.

**Hand in:** the plan, loop script or exact list of commands, search CSV, and successful run directories with Step 7 artifacts.

**Pass:** the table contains each planned combination exactly once; successful entries match their saved metrics; unsuccessful entries contain a real error reason. At least one valid candidate exists. All runs use training data only for parameter fitting and identical metric definitions. A completed search is a budget-limited comparison, not proof that every objective was optimized to convergence.

## Step 9 — Check optimization sensitivity and select one candidate (`p02-i05b`)

- [ ] **Do:** Rank successful runs by validation MSE. For the two best runs (or the only successful run), repeat from zero at twice the iteration budget, keeping all other settings fixed. Compute `abs(new_train_objective - old_train_objective) / max(1, abs(old_train_objective))` separately for latitude and longitude.

If either coordinate changes by more than `1e-3`, repeat one more doubling for that configuration. After this limit, label it `optimization-limited` if it still exceeds the threshold; do not call it converged. This is an operational sensitivity check, not a mathematical convergence guarantee.

Select the finite run with the lowest validation MSE among the original and repeat runs. For exact metric ties, prefer larger L2, then smaller layer, then smaller iteration budget. Write `output/p02/selection.json` with the selected run path, settings, validation score, constant-baseline score, and optimization-sensitivity status. Record these rules in the search plan before examining scores.

**Hand in:** repeat-run artifacts, the objective-change calculations, and `selection.json`.

**Pass:** another reviewer can reproduce the ranking and selection from saved values. No failed/non-finite run is eligible. If the selected run remains optimization-limited or worse than the constant predictor, state that explicitly; the mechanics pass, but performance improvement remains open. No hidden-test access, train/validation merging, or unrecorded extra search is allowed in this workflow.

## Step 10 — Verify the selected file in a fresh process (`p02-i06`)

- [ ] **Do:** Write `main/check_world_export.py` accepting a run directory. Load its layer from `config.json`, its raw validation features, and its `.npz` using `allow_pickle=False`. Read the saved prediction CSV independently.

**Hand in:** the script, its exact invocation, and `output/p02/export-check.txt`.

**Pass:** assert all of the following, then print PASS and the recomputed validation MSE:

```text
archive keys == {weights, bias}
weights.shape == (2, 2560); bias.shape == (2,)
both arrays have dtype float64 and contain only finite values
raw_X @ weights.T + bias has shape (130, 2) and is finite
predictions match saved CSV predictions with rtol=1e-9, atol=1e-8
recomputed MSE matches metrics.json with the same tolerance
CSV true coordinates equal the source labels in latitude/longitude order
```

The initial workflow has no preprocessing. If you later add standardization, fit it on training features only and export `W_raw = W_scaled / scale[None, :]`, `b_raw = b_scaled - W_raw @ mean`; replace zero scales with 1. Require the same raw-feature prediction comparison to pass. Scaling target values needs its own inverse transform and is outside this initial checklist.

## Step 11 — Reproduce and record the candidate (`p02-i07`)

- [ ] **Do:** Run the selected configuration from the repository root in a fresh Python process and a fresh output directory. Run Step 10 on this repeat. Compare its validation predictions with the selected run using `rtol=1e-9, atol=1e-8` rather than comparing archive bytes or elapsed times.

Copy the verified selected archive to `output/p02/world.npz`; write its layer as a single integer in `output/p02/world-layer.txt`. Update the lab README with the exact numeric training command, selected source-run path, layer, validation MSE, constant-baseline MSE, verification command, and any optimization limitation.

**Hand in:** repeat command/output, prediction comparison, the two candidate files, and README diff.

**Pass:** the fresh-process export check and prediction comparison pass; the layer file agrees with `selection.json`; copied weight and bias arrays equal those of the selected source artifact; all recorded paths exist. Code and README can be versioned while generated run evidence stays under ignored `output/`. Preparing or uploading a full course submission is a separate task.

## Finish line

All eleven steps have review evidence; the selected artifact maps raw features from one recorded layer to latitude/longitude; rerunning the recorded command reproduces its predictions. No Task 2 performance has been asserted by writing this checklist. Begin by handing in Step 1, then proceed in order.
