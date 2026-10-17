# Lab 1 — Linear probes

For Phase 1 report experiments, see [the questions 1–3 guide](docs/p01/p01_guide_questions.md).

For Task 2, follow the [minimal main checklist](docs/p02/p02_checklist_main.md): train a working coordinate predictor, make a small validation comparison, and export the required weights and layer. The [roadmap](docs/roadmap.md) now follows these priorities; the earlier detailed guides are optional references. Regression/CLI checks (`p02-i00`) and input checks (`p02-i01`) passed on October 15. No selected Task 2 model has been verified in this checklist update. Additional engineering gates from the former eleven-step checklist are retired.

Status: linear-regression fixes pass focused checks, including the stale-parameter regression covered in [p01-i03 review-r03](docs/p01/p01-i03_review-r03.md). Logistic regression is implemented but awaits review; full-data experiments remain pending.

Start with [the quick guide](docs/reference_quickguide.md) for reading order, file roles, and a time budget. The [current course repository](https://github.com/ChangshuoShen/USTC-AI3002-26fall/) lists October 21, 2026 as the deadline (checked October 9), conflicting with October 31 in the supplied `main/README.md`. Plan for October 21 and confirm through class notices.

- Inputs: originals in `backups/`, handouts in `docs/`, supplied code and immutable datasets in `main/`.
- Git policy: datasets, original archives, handout PDFs, and report build products stay local. See [input recovery and verification](docs/INPUTS.md); code, report source, and selected submissions remain eligible for tracking.
- Specification: `docs/instruction.pdf`; `../../homeworks/hw1/docs/HW1-26.pdf` is separate supporting theory homework.
- Main implementation: `main/model.py`; training entry points: `main/train1.py` and `main/train23.py`.
- Planned deliverables: code, PDF report, two `.npz` parameter files and layer numbers. No final deliverables selected yet.
- Environment: reuse the root `.venv`; NumPy/pandas for core scripts, scikit-learn/matplotlib for comparisons and plots. Dependency setup is not part of this orientation task.

The current training CLI can be inspected from the course repository root:

```bash
.venv/bin/python assignments/labs/lab1/main/train23.py --help
```

For training, pass the task/layer and explicit `--output_dir`, `--lr`, `--l1`, `--l2`, and `--max_iter` settings. Record the actual selected command and score after the experiment; no training settings are claimed as validated here.

Task 2 Step 2 (`p02-i01`) passed on October 15. Reproduce the six-pair input validation from the course root with `.venv/bin/python assignments/labs/lab1/main/p02_check_world.py`. Evidence: `output/p02/input-check.txt`. This validates shapes, types, finite values, coordinate bounds, and target order/equality; it does not independently prove the semantic alignment of supplied feature rows.

Task 2 numerical diagnosis (October 16): [NaN review](docs/p02/p02-i03_review_nan.md) identifies an excessive layer-11 learning rate and records a finite 10,000-update rerun at a smaller rate. The notebook correction and selection of a valid exported artifact remain pending.

For the next preprocessing decision, see the [standardization guide](docs/p02/p02-i05_guide_standardize.md): a single pilot, shared helpers in `train23.py`, and raw-feature parameter export. Training code is unchanged by this documentation update.

Standardization review (October 17): [review findings](docs/p02/p02-i05_review_standardization.md) confirm correct world preprocessing and raw-feature export. Two truth-branch regressions need correction: inconsistent feature scales and undefined export variables.

The [Task 2 comparison review](docs/p02/p02-i05_review_comparison.md) identifies four fixes before the grid search: supply parser positionals, preserve the selected model, reject non-finite results before export, and save the results table under `output/p02/`.

## Running the Task 2 comparison

The comparison runner now gives each invocation a new timestamped batch under `output/p02/comparison/`. Each configuration has its own directory containing `config.json`, `result.json`, and a successful run's `world_layer<L>.npz`. `comparison.csv` is updated after every attempt. The batch's `selected/` directory holds the best finite model so far as `world.npz`, its `world-layer.txt`, and `selection.json`, which identifies the source run. A numerical failure is recorded and skipped; an interruption preserves completed results. Restarting creates a new batch rather than resuming the old one.

Run the current 27-configuration follow-up grid from the course root:

```bash
.venv/bin/python assignments/labs/lab1/main/p02_comparison.py
```

The current defaults use three layers, L1/L2 values `[0.2, 0.3, 1.0]`, learning rate `0.0001`, and 10,000 updates. At seven seconds per run, 27 runs take approximately three minutes, excluding overhead; actual runtimes vary. Keep the previous selected model as a baseline. See the [comparison notes](docs/p02/p02-i05_log_comparison.md) for the initial result. To divide layers between two PCs with the same code, dependencies, and input files:

```bash
# PC 1
.venv/bin/python assignments/labs/lab1/main/p02_comparison.py --layers 11 23
# PC 2
.venv/bin/python assignments/labs/lab1/main/p02_comparison.py --layers 35
```

Each PC selects its own batch winner. Compare those winners' MSEs and retain the lower-scoring model together with its layer and settings. Local files are not automatically synchronized. Optional `--l1`, `--l2`, and `--lr` accept lists; `--max_iter` changes the update budget and `--output_dir` sets the batch parent.

The standalone `train23.py` now rejects invalid training settings, stops world training on floating-point overflow, rejects non-finite exports, and refuses to overwrite an existing archive. Choose a new `--output_dir` for a repeat run. The truth branch also retains raw inputs consistently and supplies the correct export variables.

Verification: four focused checks passed for separate outputs, best-model preservation, failed/all-failed runs, interruption handling, export equivalence, and overwrite protection. A two-configuration, 20-update layer-11 smoke run passed on real data using temporary outputs; the full grid has not been run by this change. Reproduce the focused checks with:

```bash
.venv/bin/python assignments/labs/lab1/main/p02_test_comparison.py
```

The older terminal log records scores but cannot restore overwritten per-configuration weights. Keep it as historical evidence; use the new batch outputs for selecting the final artifact.
