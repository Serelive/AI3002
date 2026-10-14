# p01-i03 review-r03 — Stale parameters during training

**Finding: `self.predict(features)` uses different parameters from the ones being optimized.** Fixed in the linear-regression model only (October 14, 2026).

## Why the MSE grew

`fit()` updates local variables `weights` and `bias`. The attributes `self.weights` and `self.bias` are assigned only after the loop. However, `predict()` reads those attributes, so its predictions remain unchanged throughout training.

The key distinction is **local parameters versus stored parameters**. `features @ self.weights + self.bias` is equivalent to `self.predict(features)`, but the original gradient used `features @ weights + bias`, without `self`.

On a fresh model, stored parameters are zero. With no regularization, the residual therefore stays `-targets` and every iteration repeats the same update instead of correcting the current prediction. On the supplied toy data, 10,000 iterations produced `weights=[500,0]`, `bias≈200`, and **MSE≈412,106**.

## Fix

Compute the residual once from the arguments passed to `_gradient()`:

```python
residual = features @ weights + bias - targets
```

Use this residual for both gradients, preserving the factor of two, L1/L2 penalties, and simultaneous updates. This keeps the existing local-parameter design consistent; reusing `predict()` would require changing how training maintains model state.

## Verification

Added `main/test_linear_regression.py`. All three tests passed:

- Two successive updates give `w=b=0.32` for `X=[[1]]`, `y=[1]`, and learning rate `0.1`; this catches stale predictions after the first update.
- Weight and bias gradients match numerical differentiation with no penalty, L1, L2, and both, even when stored parameters differ from the gradient arguments.
- Toy-data fitting and refitting recover `weights≈[2,-1]`, `bias≈1`, with MSE below `1e-16` and the expected prediction shape.

Reproduce from the repository root:

```bash
.venv/bin/python assignments/labs/lab1/main/test_linear_regression.py
```

The logistic-regression class was verified unchanged from the start of this review. Its correctness and full-dataset training were not assessed.
