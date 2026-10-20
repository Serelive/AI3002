# p02-i05 review: training and hyperparameter comparison

Scope: the current world workflow in `main/train23.py` and `main/p02_comparison.py`. The truth branch remains deferred. Line references describe the reviewed working files; no implementation was changed.

**Verdict:** fix argument construction, preservation of selected weights, and non-finite-result handling before launching the search. The world standardization and conversion back to raw-feature parameters remain correct.

## Findings, in priority order

### 1. The comparison exits before its first training run

**`p02_comparison.py:24` — high priority.** `parser.parse_args([])` requires the positional arguments `task` and `layer`. It raises `SystemExit(2)` before the following assignments execute. Supply them when parsing:

```python
args = parser.parse_args(["world", str(layer)])
```

The existing assignments for `l1`, `l2`, `lr`, and `max_iter` can then override the defaults. Constructing the parser once before the loops is sufficient.

### 2. Saved weights belong to the last run, not necessarily the best run

**`train23.py:137–145`; `p02_comparison.py:31,44–45` — high priority.** Every configuration for one layer saves to the same `world_layer<layer>.npz`. Printing the best DataFrame row does not restore its weights. The final directory therefore contains at most three last-run models, which may disagree with the selected scores.

The simplest repair is to finish the score comparison, reconstruct the best configuration, and **rerun it once into `output/p02/selected/`**, saving its settings and layer alongside the weights. Alternatively, give every configuration a distinct output directory. Either approach must make the selected score and selected archive refer to the same configuration.

### 3. Failed numerical runs are exported and included in the results

**`train23.py:141–151`; `p02_comparison.py:33–44` — high priority.** Saving occurs before MSE calculation, and neither script rejects NaN/infinity. A divergent run can overwrite a valid archive. Pandas normally skips NaN during `idxmin`, but that does not protect the saved weights or provide a valid selection when every run fails.

Compute MSE before saving. Require finite MSE, predictions, weights, and bias; if the check fails, raise a clear numerical error before `np.savez`. In the comparison loop, record that configuration as failed and continue. Select only finite scores, and report a failure clearly if no valid candidate remains.

### 4. Results use the working directory and are saved only after all runs

**`p02_comparison.py:41–42` — medium priority.** `"p02_comparison.csv"` lands in `main/` or the repository root depending on how the script is launched. A late interruption also loses all accumulated rows from disk.

Use `Path(__file__).resolve().parent.parent / "output" / "p02"`, create that directory once, and write the small results table after each completed configuration. This needs only a few lines, not an experiment-management system.

## Keep the search within the lab budget

The current grid has `3 × 5 × 5 × 5 = 375` runs. At the 30-second estimate in your notes, that is about 3 hours 8 minutes, before additional overhead. Start with `L1 = [0.0]`, a few L2 values, and a stable learning rate per standardized layer. The current grid omits zero penalties entirely. Add L1 comparisons only if time remains.

A fixed 10,000 updates with rates ranging from `1e-7` to `1e-3` can compare very different amounts of optimization progress. Use the stable pilot to set the learning rate and iteration budget before ranking regularization choices. Loading and standardizing once per layer is a useful later speed improvement, but the four fixes above take priority.

## Checks executed

- Called the actual comparison entry point: reproduced the missing-positional-arguments error and exit status 2, before any full-data training.
- Exercised the actual world training/export path with small synthetic inputs: a run with MSE `0.00359` was overwritten by one with MSE `26.9784`; only one archive remained.
- Used an intentionally excessive learning rate on the same synthetic inputs: reproduced NaN MSE and an exported archive containing non-finite parameters.
- All generated archives were temporary. The 375-run search was not launched.

**Next step:** apply the four small workflow fixes, run two configurations as a smoke check, then launch the reduced grid.
