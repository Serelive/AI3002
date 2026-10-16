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
