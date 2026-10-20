# p02-i05: standardization before hyperparameter selection

## Recommendation

**Try feature standardization once before expanding the hyperparameter search.** Centering and scaling the columns can improve gradient-descent behavior and put regularization on a comparable scale across features. Keep the existing raw-feature result as a baseline and compare validation MSE before choosing the preprocessing for subsequent runs.

Your previous NaN problem came from an excessive learning rate. Standardization changes the curvature, so choose a stable rate again; it does not automatically make `lr=0.01` safe. Highly correlated features can still make optimization slow.

## Where to put it

Add two small helpers to **`main/train23.py`**, alongside `load_split`: one to fit/apply feature standardization, and one to convert trained parameters back to raw-feature coordinates. Call them in the world branch and import them into your existing `main/p02_comparison.py` when building the comparison loop.

This keeps the CLI and comparison script consistent without another Python file. Keep `LinearRegressionModel` focused on fitting and predicting the arrays it receives. Leave `load_split` returning raw features so preprocessing is explicit and export checks can use the original inputs.

## What the helpers should do

Compute one mean and standard deviation per feature, using **training rows only**, separately for each layer:

```python
mu = train_x.mean(axis=0)             # (2560,)
scale = train_x.std(axis=0, ddof=0)    # population standard deviation
scale = np.where(scale == 0, 1.0, scale)
train_z = (train_x - mu) / scale
valid_z = (valid_x - mu) / scale
```

Use float64 arrays, train on `train_z`, and predict on `valid_z`. Reuse the training statistics for validation; estimating them separately would change the feature coordinates seen by the model. Keep latitude and longitude in degrees. Compute these arrays once per layer and reuse them across regularization settings.

The standardization helper can return `train_z, valid_z, mu, scale`. The export helper takes `W_z, b_z, mu, scale` and returns:

```python
# W_z: (2, 2560), b_z: (2,); latitude first, longitude second
W_raw = W_z / scale[None, :]
b_raw = b_z - W_raw @ mu

np.testing.assert_allclose(
    valid_x @ W_raw.T + b_raw,
    valid_z @ W_z.T + b_z,
    rtol=1e-9, atol=1e-8,
)
```

This follows by expanding `((X - mu) / scale) @ W_z.T + b_z`. Save `W_raw` and `b_raw` as the required float64 `weights` and `bias` arrays: the submitted model must accept the original features without an external scaler.

## Keep the experiment small

1. On layer 11, run one standardized pilot with `l1=0` and one L2 setting. Select a stable learning rate for `train_z` using the curvature calculation in the [NaN review](../../../../../archive/lab1/reviews/p02/p02-i03_review_nan.md), replacing `train_x` with `train_z`.
2. Compare its validation MSE with the raw-feature baseline and choose the preprocessing for the small layer/L2 comparison. Record the choice with the settings.
3. Tune L2 before adding L1. Standardization changes the penalty: `w_z = scale * w_raw`, so an L2 penalty on `w_z` weights raw coefficients by `scale**2`. Retune regularization rather than copying the raw-feature optimum.

Your draft proposes five values each for L1, L2, and learning rate. Across three layers, a full grid would require **375 runs**, about **3 hours 8 minutes** at your estimate of 30 seconds per run. A stable rate, L1 fixed at zero, and a few L2 comparisons fit the lab's time budget better.

The standardization and export formulas above were checked on a small synthetic example including a constant feature. No standardized world-model training was run for this guide; the pilot remains the next action.
