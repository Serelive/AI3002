# p02-i05 review: standardization and parameter conversion

Reviewed October 17, 2026. **The world branch is correct; the truth branch needs two fixes.** References below use the current line numbers in `main/train23.py`. No training code was changed during this review.

## Findings

1. **High priority — truth export crashes (lines 128–129, 145–148).** The truth branch assigns `weights` and `bias`, while the shared save block reads `weights_original` and `bias_original`, which are assigned only in the world branch. Running truth therefore raises `UnboundLocalError` at export. Use the same export-variable names in both branches.

2. **High priority — truth training and prediction use different feature scales (lines 125–127).** Training receives `train_x`, but prediction receives `standardized_valid_x`. The learned coefficients expect raw features, so the printed validation accuracy evaluates the wrong inputs. For the smallest Task 2-focused correction, keep truth on raw features:

   ```python
   model.fit(train_x, train_y)
   prediction = model.predict(valid_x)
   weights_original = model.weights
   bias_original = model.bias
   ```

   These lines replace the corresponding truth-branch statements. If standardizing Task 3 later, train and predict on standardized arrays and convert its parameters before export as well.

## What is correct for Task 2

- `fit_standardizers` computes column means and population standard deviations, replacing zero standard deviations with 1 (lines 35–41).
- Statistics are fitted only on training data and reused for validation (lines 79–84).
- Both coordinate models train and predict in the same standardized space (lines 108–114).
- `reverse_weights_bias` correctly implements `w_raw = w_z / std` and `b_raw = b_z - mean @ w_raw` (lines 50–57). Expanding `((X - mean) / std) @ w_z + b_z` gives exactly `X @ w_raw + b_raw`.
- The world export has latitude first, longitude second, with float64 arrays of shapes `(2, 2560)` and `(2,)`.

## Checks executed

- Synthetic features, including a constant training column: finite transforms, zero training means, unit standard deviations for varying columns, and equivalent raw/standardized predictions.
- Actual world/layer-11 data through `main()`: 20 updates, `lr=0.0001`, `l1=0`, `l2=0.01`. The temporary archive had the correct schema and finite parameters. Reloaded raw-feature predictions matched independently refitted standardized-model predictions with `rtol=1e-9, atol=1e-8`. Validation MSE was `2095.1133`; this brief run checked integration, not model selection.
- Actual truth branch with small synthetic inputs: confirmed the scale mismatch and reproduced the export exception. Temporary archives were removed after checking.

**Next action:** apply the two truth-branch corrections above. The Task 2 standardization helpers are ready for the small hyperparameter comparison; use a stable learning rate for the transformed features.
