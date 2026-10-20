# p01-i03 — Linear regression review

Reviewed `main/model.py` against `docs/instruction.pdf` §2.1 on October 13, 2026. Scope: p01-i00–i02; logistic regression is not yet in scope. **Result: fix the three issues below before proceeding.** Line numbers refer to the reviewed code.

## Findings

1. **High — floor division prevents learning (lines 45–46).** `1 // N` is zero for every `N > 1`. Both data gradients vanish; zero initialization also makes the regularization gradient zero, so training leaves all parameters at zero. Use floating-point division.
2. **High — the MSE gradients need a factor of two (lines 45–46).** Replacing `//` with `/` alone is insufficient. For residual `r = X @ w + b - y`, the handout requires `grad_w = (2 / N) * (X.T @ r) + l1 * sign(w) + 2 * l2 * w` and `grad_b = 2 * mean(r)`. Keeping `1 / N` changes the balance between data fit and regularization; it is not merely a learning-rate change when penalties are enabled.
3. **Medium — parameter updates are not simultaneous (lines 29–30).** The second `_gradient()` call uses the new weights and old bias. Compute `grad_w, grad_b` once from the old parameters, then update both. This also avoids duplicate matrix operations.

## Executed checks

Used the root `.venv` with NumPy 2.5.3; all examples are deterministic.

| Check | Observed result |
| --- | --- |
| Supplied `train1.py` | Linear MSE **6.0000**, then the expected `NotImplementedError` from unfinished logistic regression. |
| `X=[[1.]]`, `y=[1.]`, zero parameters, no penalties | Gradient `(-1, -1)`; required `(-2, -2)`. |
| Same data, `lr=0.1`, `max_iter=1` | `(w,b)=(0.1,0.09)`; required `(0.2,0.2)`. The unequal updates expose finding 3. |
| Prediction with `w=[2.]`, `b=3`, `X=[[1.],[2.]]` | `[5.,7.]`, shape `(2,)`: passed. |
| Zero data residual, `w=[2.]`, `l1=0.3`, `l2=0.4` | Weight gradient `1.9`, bias gradient `0`: passed. |

Reproduce the supplied example from the repository root:

```bash
.venv/bin/python assignments/labs/lab1/scr/train1.py
```

The iteration limit is an acceptable stopping rule, and leaving the bias unregularized is correct. After fixing the findings, rerun the one-step check and verify that the supplied linear example approaches `w=[2,-1]`, `b=1`, with near-zero MSE. Those post-fix checks have **not** been executed. No implementation files were modified.
