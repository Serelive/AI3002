# Lab 1 — Linear probes

For Phase 1 report experiments, see [the questions 1–3 guide](docs/p01/p01_guide_questions.md).

For Task 2, start with the [actionable main checklist](docs/p02_checklist_main.md), then use the [roadmap](docs/roadmap.md) and main-body guides in [English](docs/p02/p02_guide_main-eng.md) and [Chinese](docs/p02/p02_guide_main-zh.md). The checklist provides eleven separately reviewable steps, based on the October 15 CLI. Existing training options are implemented; completion of the training, selection, and export steps requires the listed review evidence. The guides distinguish existing commands from proposed options and defer questions 4–7. No Task 2 submission artifact has been selected.

Status: linear-regression fixes pass focused checks, including the stale-parameter regression covered in [p01-i03 review-r03](docs/p01/p01-i03_review-r03.md). Logistic regression is implemented but awaits review; full-data experiments remain pending.

Start with [the quick guide](docs/reference_quickguide.md) for reading order, file roles, and a time budget. The [current course repository](https://github.com/ChangshuoShen/USTC-AI3002-26fall/) lists October 21, 2026 as the deadline (checked October 9), conflicting with October 31 in the supplied `main/README.md`. Plan for October 21 and confirm through class notices.

- Inputs: originals in `backups/`, handouts in `docs/`, supplied code and immutable datasets in `main/`.
- Git policy: datasets, original archives, handout PDFs, and report build products stay local. See [input recovery and verification](docs/INPUTS.md); code, report source, and selected submissions remain eligible for tracking.
- Specification: `docs/instruction.pdf`; `../../homeworks/hw1/docs/HW1-26.pdf` is separate supporting theory homework.
- Main implementation: `main/model.py`; training entry points: `main/train1.py` and `main/train23.py`.
- Planned deliverables: code, PDF report, two `.npz` parameter files and layer numbers. No final deliverables selected yet.
- Environment: reuse the root `.venv`; NumPy/pandas for core scripts, scikit-learn/matplotlib for comparisons and plots. Dependency setup is not part of this orientation task.

After installing dependencies and implementing the model stubs, run from the course repository root:

```bash
.venv/bin/python assignments/labs/lab1/main/train1.py
.venv/bin/python assignments/labs/lab1/main/train23.py world 11 assignments/labs/lab1/output/world.npz
.venv/bin/python assignments/labs/lab1/main/train23.py truth 11 assignments/labs/lab1/output/truth.npz
```

These are starting commands, not executed or validated training results; layer 11 is an initial baseline choice. Record configurations, seeds, and results when experiments begin.
