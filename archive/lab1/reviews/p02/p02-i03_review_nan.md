# p02-i03 review: NaN parameters and validation MSE

Reviewed October 16, 2026 against the current `main/p02_scaffold.ipynb` and `main/model.py`. Code and notebook were not modified.

## Main finding: the learning rate causes divergence

Both training cells use `lr=0.01`, `l1=l2=0.01`, and `max_iter=10000`. The gradient implementation matches the specified mean-squared-error objective; the problem is the update size for the raw layer-11 features, not the validation MSE calculation.

With augmented features `A = [X, 1]`, the smooth part of the objective has Hessian

```text
H = 2 A.T @ A / N + 2*l2*diag(1, ..., 1, 0).
```

Its largest eigenvalue is between `3674.6265` and `3674.6465`. For smooth quadratic gradient descent, the stable step range is `0 < lr < 2/lambda_max(H)`, whose upper limit here is approximately **0.00054427**. The notebook's `0.01` is about **18.4 times that limit**. The L1 term adds a bounded subgradient; it does not prevent the observed explosive updates. The smooth stability formula alone is not a convergence guarantee for L1 subgradient descent.

## Executed evidence

Loaded the actual world/layer-11 training and validation arrays through `load_split`: all inputs are finite, and features/targets are already `float64`.

Replaying the current gradient updates from zero with the notebook's settings:

| Completed update | Latitude model: largest absolute weight |
| --- | ---: |
| 1 | 6.826 |
| 2 | 231.749 |
| 3 | 8,297.201 |
| 10 | 6.188 × 10^14 |

Both coordinate models first acquired non-finite parameters at **update 197** in this run. Continuing invalid arithmetic explains the all-NaN parameters and predictions in the saved notebook output. More iterations do not fix this, and converting to float64 again is not a solution.

Changing **only the learning rate** to `0.0002449215190885182`, while retaining `l1=l2=0.01` and 10,000 updates, produced finite parameters for both coordinates and **validation MSE 160.2110451130169** (squared degrees). This is a numerical-stability check, not evidence of the best model or full convergence. No trained archive was saved during this review.

## Minimal correction

After loading `train_x`, compute the rate below and pass it to both model constructors. Apply the change to both duplicated training cells, or run only one corrected training cell.

```python
A = np.column_stack((train_x, np.ones(len(train_x))))
largest_eigenvalue = np.linalg.eigvalsh(A @ A.T)[-1]
L_bound = 2 * largest_eigenvalue / len(train_x) + 2 * l2
lr = 0.9 / L_bound
```

`A @ A.T` is only `(500, 500)` and has the same nonzero eigenvalues as `A.T @ A`; this avoids building a `(2561, 2561)` matrix. For this unchanged layer and L2 value, directly setting `lr = 0.0002449215190885182` reproduces the tested rate. Rerun the training cell from its model construction, not just the prediction cell; `fit()` initializes parameters from zero.

Before `np.savez`, add a small guard so a failed run cannot silently export unusable weights:

```python
assert np.isfinite(weights).all() and np.isfinite(bias).all()
assert np.isfinite(prediction).all()
```

## Separate issue: output path

The notebook's recorded output is `assignments/labs/output/world/world_layer11.npz`, outside `lab1`. This comes from `Path(os.getcwd()).parent.parent`. It does not cause NaN, but misplaces the artifact. With the notebook working directory set to `lab1/main`, use `Path.cwd().parent / "output" / "p02"`, and print the resolved path before saving. The previously exported NaN archive is not a valid submission candidate; select only a newly trained, finite artifact.
