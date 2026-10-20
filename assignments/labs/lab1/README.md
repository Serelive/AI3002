# Lab 1 — Linear probes

For Phase 1 report experiments, see [the questions 1–3 guide](docs/p01/p01_guide_questions.md).

For Task 2, follow the [minimal main checklist](docs/p02/p02_checklist_main.md): train a working coordinate predictor, make a small validation comparison, and export the required weights and layer. The [roadmap](docs/roadmap.md) now follows these priorities; the earlier detailed guides are optional references. Regression/CLI checks (`p02-i00`) and input checks (`p02-i01`) passed on October 15. The learner considers Phase 2 sufficiently implemented; further training/refinement will continue on the 107 platform. Promising settings are layers 11/35, L1 and L2 around 0.3–1.0, and learning rate around 0.0001. These ranges are not a single final submission selection. Additional engineering gates from the former eleven-step checklist are retired.

Status: linear-regression fixes pass focused checks, including the stale-parameter regression covered in [p01-i03 review-r03](../../../archive/lab1/reviews/p01/p01-i03_review-r03.md). Task 2 experiments have been run by the learner. Logistic regression, CLI settings, early stopping, and raw-feature exports now pass focused checks; Task 3 tuning remains.

Start with [the quick guide](docs/reference_quickguide.md) for reading order, file roles, and a time budget. The [current course repository](https://github.com/ChangshuoShen/USTC-AI3002-26fall/) lists October 21, 2026 as the deadline (rechecked October 20), conflicting with October 31 in the supplied `main/README.md`. Plan for October 21 and confirm through class notices.

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

Task 2 numerical diagnosis (October 16): [NaN review](../../../archive/lab1/reviews/p02/p02-i03_review_nan.md) identifies an excessive layer-11 learning rate and records a finite 10,000-update rerun at a smaller rate. This is historical diagnosis; subsequent Task 2 work added standardization, stable runs, and separate experiment outputs.

For the next preprocessing decision, see the [standardization guide](docs/p02/p02-i05_guide_standardize.md): a single pilot, shared helpers in `train23.py`, and raw-feature parameter export. Training code is unchanged by this documentation update.

Standardization review (October 17): [review findings](../../../archive/lab1/reviews/p02/p02-i05_review_standardization.md) confirm correct world preprocessing and raw-feature export. The two truth-branch scale/export regressions in that review were corrected later; CLI settings and the later early-stopping fixes are now implemented and tested.

The [Task 2 comparison review](../../../archive/lab1/reviews/p02/p02-i05_review_comparison.md) documents four subsequently implemented fixes: supply parser positionals, preserve the selected model, reject non-finite results before export, and save the results table under `output/p02/`.

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

## Starting Task 3

Use the [p03 guide and conversation handoff](docs/p03/p03_guide_main.md). It covers the handout requirements, current code issue, a short implementation plan, required export format, report evidence, and transfer to the 107 platform. Local truth inputs were checked: 5,088 balanced training rows and 300 balanced validation rows, with 2,560 features at layers 11/23/35. No Task 3 training was run in preparing this handoff.

### Task 3 iteration fixes (`p03-i01`)

Implemented the [iteration review](docs/p03/p03-i01_review_iteration.md). Both
models now check the final update, retain the lowest-loss evaluated checkpoint
independently of the patience threshold, and scale gradient vectors after the
matrix–vector product. Stopping still monitors regularized training loss every
20 updates, with patience 5 and tolerance `1e-6`; small improvements accumulate
against the last significant-improvement reference. The models expose `n_iter_`,
`best_iter_`, and `stop_reason_`, and `train23.py` prints these after training.

The truth branch now trains and validates on features standardized using training
statistics, then exports raw-feature weights and bias. Default outputs are under
`output/<task>/`, with existing-file protection. Existing artifacts under
`main/output/` have not been moved or selected for submission.

Reproduce the focused checks from the repository root:

```bash
.venv/bin/python assignments/labs/lab1/main/p03_test_iteration.py
.venv/bin/python assignments/labs/lab1/main/p01_test_linear-regression.py
.venv/bin/python assignments/labs/lab1/main/p02_test_comparison.py
```

All 12 tests passed. Coverage includes final-update boundaries, patience with
small improvements, non-finite initial loss, default paths, prior regression and
comparison behavior, and a real layer-11 truth run. That deterministic 21-update
smoke run used `lr=0.01`, `l1=l2=0.01` and obtained validation accuracy 0.6800;
reloaded raw-feature probabilities matched the in-memory predictions, and export
shapes/dtypes passed. Its temporary artifact was removed automatically. This is
execution validation, not a tuned model selection. The older linear toy-fit test
now uses tolerances appropriate to training-loss early stopping.

For a separate pilot artifact, run:

```bash
.venv/bin/python assignments/labs/lab1/main/train23.py truth 11 \
  --lr 0.01 --l1 0.01 --l2 0.01 --max_iter 100 \
  --output_dir assignments/labs/lab1/output/p03/i01-pilot
```

## HPC continuation

Follow the [107 Slurm handoff](../../../docs/HPC.md) for environment setup, dataset transfer, a compute-node check job, and training commands. `scripts/slurm/lab1.sbatch` (from the repository root) supports `check`, `world`, `truth`, and `comparison`; each job gets its own output directory and environment record. Resolved reviews are retained in [the archive](../../../archive/README.md). Existing `main/output/` artifacts remain local and ignored.
