# Lab 1 / p02: actionable guide to the main body of Task 2.

Code fragments below are implementation examples, not a complete script.
Chinese companion: [p02_guide_main-zh.md](p02_guide_main-zh.md).

## 0. Scope, sources, and current status
Read docs/instruction.pdf sections 2.1, 2.2, 3 and Appendix C.1, then
main/model.py and main/train23.py. Paths in this guide are relative to
assignments/labs/lab1 unless explicitly stated otherwise. Shell commands run
from the course repository root. Follow docs/roadmap.md increments p02-i00-i07.

Deliver a linear map from one layer's 2,560 features to [latitude, longitude].
Keep the LLM fixed; supplied features need no GPU or model download. Questions
4-7, map drawing, and interpretation of representations are deferred. Selecting
layers and regularization is still necessary for the main training task.

Instructor requirements: use a single layer (0-35); export float64 weights of
shape (2, 2560) and bias of shape (2,), with latitude first. Report the layer
separately. Final weights may come from library training, but Task 1 still
requires handwritten gradient-descent training with L1 and L2 support.

Planning choices below (baseline, search grid, logs) are recommendations, not
additional grading rules. The course repository lists October 21, 2026 as the
deadline, checked October 14; main/README.md says October 31. Plan for October
21 and check class notices. Source:
https://github.com/ChangshuoShen/USTC-AI3002-26fall/
The upstream lab directory could not be fetched during this check; detailed
requirements here follow the supplied local instruction.pdf.

Verified locally on October 14: all six world feature arrays are finite float16
arrays with the expected shapes; both CSV files have the expected four columns
and no missing values. Python/NumPy/pandas versions: 3.14.4 / 2.5.3 / 3.0.6.
No Task 2 training results were generated while preparing this guide.

## 1. p02-i00: establish the starting point
Run the existing focused linear-regression checks:

    .venv/bin/python assignments/labs/lab1/main/test_linear_regression.py
    .venv/bin/python assignments/labs/lab1/main/train23.py --help

The current model resets parameters to zero in fit(), takes max_iter gradient
steps, and has no convergence log or early stopping. Current defaults are
lr=0.01, max_iter=10000, l1=l2=0. These are not validated for world features.
The current train23.py accepts only task, layer, and output positional arguments.
Its world branch already trains two models and exports the correct arrangement.
Do not reimplement that structure. Preserve the truth branch for Task 3.

Done when: you can trace load_split -> fit -> predict -> MSE -> np.savez and
explain each shape. A passing toy test does not establish full-data stability.

## 2. p02-i01: inspect the data contract
Inputs in main/datasets/world/:

    train.csv                 500 rows; sentence, country, latitude, longitude
    valid.csv                 130 rows; same columns
    train.layer{11,23,35}.npy  each (500, 2560), float16
    valid.layer{11,23,35}.npy  each (130, 2560), float16

CSV row i labels feature row i. Never independently sort, filter, or shuffle
one file. Row counts alone cannot prove semantic alignment; preserve supplied
order. Country and sentence are metadata, not extra probe input features.
Coordinates are degrees, with north/east positive.

Reuse load_split("world", "train", layer) and the matching validation call.
It converts features and targets to float64; check shape, dtype, finite values,
and target latitude/longitude ranges before training. Require layer in
(11, 23, 35) for the supplied-data workflow and fail clearly for absent files.
Keep raw files unchanged. Training fits parameters; validation selects settings;
the hidden test is not available for tuning. Do not merge train and validation
in the baseline workflow.

## 3. p02-i02: connect equations to code
For X of shape (N, D) and Y of shape (N, 2), fit two independent objectives:

    L_k = mean((X @ w_k + b_k - Y[:, k])**2)
          + l1 * sum(abs(w_k)) + l2 * sum(w_k**2), k = 0, 1

Each w_k has shape (D,); each b_k is scalar. Bias is not regularized. The
squared-error objective separates by output, so no coupled optimizer is needed.

    latitude_targets = train_y[:, 0]       # (N,), not (N, 1)
    longitude_targets = train_y[:, 1]
    prediction = np.column_stack((lat_pred, lon_pred))  # (N, 2)
    W = np.stack((lat_model.weights, lon_model.weights))  # (2, D)
    b = np.array((lat_model.bias, lon_model.bias))        # (2,)
    prediction_from_parameters = valid_x @ W.T + b       # (N, 2)

column_stack turns two prediction vectors into columns. stack adds a row axis
to the two weight vectors. W.T changes (2, D) into (D, 2); broadcasting adds
the two bias values to every row. A target shaped (N, 1) can accidentally
broadcast against (N,) predictions to create (N, N) residuals.

## 4. p02-i03: make a stable, observable baseline
First add --lr, --max-iter, --l1, --l2 to train23.py and pass them explicitly to
both coordinate models. Record them. These flags do NOT exist yet. Reject
nonpositive learning rates/iteration limits and negative regularization.
Use raw float64 features initially, layer 11, and l1=l2=0.

Inside fit(), add optional periodic training-objective logging and finite-value
checks for loss, gradients, and parameters. Fail before exporting invalid
weights. Log the final completed iteration and stopping reason. Keep validation
out of gradient calculations. Start with a short run, inspect its loss, then
increase the iteration budget; do not launch a large grid with an unstable rate.

A conservative rate for the smooth objective (l1=0) can be obtained from:

    A = np.column_stack((train_x, np.ones(len(train_x))))
    L_bound = 2 * np.sum(A * A) / len(A) + 2 * l2
    lr = 0.9 / L_bound

The Hessian is 2 A.T @ A / N plus the L2 diagonal (bias excluded).
The squared Frobenius norm bounds the squared spectral norm, so this is a safe
upper bound on curvature, but may yield slow progress. Compute it once per
configuration. A tighter spectral bound or a carefully checked larger rate can
follow if necessary. This smooth convergence argument does not apply to L1;
fixed-step subgradient descent can oscillate near zero. Diagnose that behavior
before interpreting an L1 comparison.

Current executable interface, shown for reference, is:

    .venv/bin/python assignments/labs/lab1/main/train23.py world 11 assignments/labs/lab1/output/p02/baseline-layer11.npz

It uses the unverified defaults above. After adding options, explicitly pass
the numerically computed rate and chosen iteration limit. Do not treat the
reference command as a confirmed stable baseline or a measured result.

Done when: a full-data run finishes with finite predictions, saved parameters,
and a reproducible configuration; training loss decreases for the smooth run.

## 5. p02-i04: measure the baseline and preserve evidence
Compute training and validation errors separately:

    mse_by_coordinate = np.mean((prediction - targets)**2, axis=0)  # (2,)
    mse = float(mse_by_coordinate.mean())
    rmse_by_coordinate = np.sqrt(mse_by_coordinate)

The script's MSE averages over both rows AND coordinates: it is
(MSE_latitude + MSE_longitude) / 2, in squared degrees. RMSE is in degrees.
Neither is distance in kilometres. The handout does not specify an exact hidden
test scoring formula; this MSE is the supplied script's local comparison metric.
Do not clip or wrap predictions silently; evaluate the exported linear map.

Compare against a constant predictor fitted using training targets only:

    mean_coordinate = train_y.mean(axis=0)
    baseline_prediction = np.broadcast_to(mean_coordinate, valid_y.shape)

This gives a simple sanity reference. Poor improvement requires diagnosis, not
an invented pass threshold. Check convergence, output order, and feature/label
alignment before expanding experiments.

Create output/p02/ only when experiments begin. For each distinct run, retain:

- metrics.csv row: run_id, layer, l1, l2, lr, max_iter, actual iterations,
  stopping reason, train/valid MSE and per-coordinate errors, elapsed seconds;
- config.json or equivalent: exact command, preprocessing, package versions,
  initialization, source revision, and seed if randomness is introduced;
- weights .npz, training log, and validation predictions in original row order
  with row index, true latitude/longitude, predicted latitude/longitude.

Zero-initialized full-batch training has no random sampling; record that rather
than claiming an unused seed. If shuffling or randomized methods are added,
choose and record a fixed seed (for example 42). Avoid overwriting distinct runs.

## 6. p02-i05: choose layer and regularization within a small budget
After the baseline is stable, compare layers 11, 23, 35 using the same protocol.
An initial suggested L2 grid is {0, 1e-4, 1e-2, 1, 100}, with l1=0. It is not a
guarantee of a good range; feature scale matters. Recompute a stable rate for
each layer/L2 value and check convergence so a slow run is not mistaken for a
bad model. If the best result is at a grid boundary, extend modestly once.
Start with one shared regularization setting for both coordinate models.

Rank finite, adequately optimized runs by validation MSE and inspect both
coordinate errors. Training error alone is not a selection criterion when
D=2560 exceeds N=500. Record a tie rule before searching (for example prefer
the larger L2 for numerically tied validation MSE). Limit repeated validation
searches; validation performance after selection is not an unbiased test score.
A small L1 comparison is optional for this main workflow; Task 1's requirement
to implement both penalties remains. Library-trained final weights are allowed
by section 2.2, but are not required to establish the handwritten baseline.

## 7. Optional preprocessing: preserve raw-feature inference
Only add feature standardization if it solves an observed optimization issue.
Fit mean mu and scale s on TRAIN features only; replace zero standard deviations
by 1. Apply the same transformation to validation. Scaling changes the meaning
of the regularization penalty, so label such runs separately.

The exported artifact must work on raw features without an external scaler.
If Z=(X-mu)/s and the learned parameters are W_z, b_z, fold the transform in:

    W_raw = W_z / s[None, :]
    b_raw = b_z - W_raw @ mu
    np.testing.assert_allclose(
        valid_x @ W_raw.T + b_raw,
        ((valid_x - mu) / s) @ W_z.T + b_z,
        rtol=1e-9, atol=1e-8,
    )

The tolerance is a suggested float64 check, not an instructor requirement.
Keep targets in degrees in the initial workflow; target scaling would require
another inverse transformation. Do not export standardized-space weights as
though they applied directly to the provided features.

## 8. p02-i06-i07: reload, verify, and freeze a candidate
After saving, reload from disk in a fresh process with allow_pickle=False:

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

Here prediction is the saved pre-export validation prediction for the same run,
and valid_x comes from that run's chosen layer. Recompute MSE after reloading.
Matching metrics alone are weaker evidence than matching every prediction.
Also check latitude is row 0 and longitude row 1 against the trained models.

Preserve one selected candidate as output/p02/world.npz with its layer integer
in output/p02/world-layer.txt and configuration/metrics beside it. These names
are local conventions, not mandated filenames. Reproduce that candidate in a
fresh process before deliberately copying final files to submission/.
Update the lab README with the exact command, layer, metrics, and limitations.
Do not claim Task 2 report completion: questions 4-7 remain pending, as do Task 3
and full-lab packaging. A validation improvement establishes predictive utility
on that split; it does not by itself prove how the LLM uses geographic knowledge.

## Troubleshooting order
Missing input: check docs/INPUTS.md and file provenance; do not fabricate data.
Shape error: inspect (N,), (N, 2), (2, D), (2,) and coordinate order.
NaN/inf or rising smooth loss: check float64 conversion and learning rate first.
Flat loss: inspect gradient magnitude, learning rate, and completed iterations.
Low train / high validation error: verify convergence, then consider L2/layer.
L1 oscillation: inspect step size and objective trace before extending runtime.
Reload mismatch: check layer, transpose, bias, row order, preprocessing folding.

Finish line: finite reproducible predictions, a documented validation-selected
configuration, a verified raw-feature .npz artifact, and a recorded layer.
