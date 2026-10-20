# Lab 1 quick guide

Here, `lab1` means `assignments/labs/lab1`; paths below are relative to it. The lab trains linear probes on supplied LLM features to predict geographic coordinates and sentence truth.

## 1. Reading order

1. **`scr/README.md`** — a two-minute overview. Its October 31 end date conflicts with the [current course repository](https://github.com/ChangshuoShen/USTC-AI3002-26fall/), which lists **October 21, 2026** as the Lab 1 deadline (checked October 9). Plan for October 21 and check class notices for confirmation.
2. **`docs/LAB1.pdf`** — read §3 first for deliverables and grading, then §§1–2 for the tasks and nine report questions. Read Appendix C.1 for NumPy file formats; consult Appendix A only as needed. `scr/README.pdf` is an identical copy, so skip rereading it.
3. **`docs/HW1-26.pdf`** — supporting theory, a separate homework rather than the lab specification. Prioritize Q2 (separate coordinate regressions), Q3 (gradients and regularization), and Q4 (logistic regression); Q1 provides generalization background. You need not finish this homework before starting the lab.
4. **`scr/model.py` → `scr/train1.py` → `scr/train23.py`** — understand the model interface, the small sanity-check example, then real-data loading, validation, and weight export.
5. **`scr/datasets/` and `scr/report.template.tex`** — inspect CSV columns and examples, then skim the report outline before experimenting so you collect evidence for all nine questions.

Leave `extract_intrep.py` and Appendix B until you choose to extract additional features. Appendices D–E are optional background.

## 2. File map

```text
lab1/
├── backups/                 Original HW1-26.pdf, LAB1.pdf, LAB1.zip; preserve
├── docs/                    Working handouts and this guide
└── scr/
    ├── README.md / README.pdf  Overview / full lab instructions
    ├── model.py             Core implementation: fit() and predict() stubs
    ├── train1.py            Small synthetic-data sanity check
    ├── train23.py           world/truth training, validation, .npz export
    ├── datasets/
    │   ├── world/           Coordinates: 500 training / 130 validation rows
    │   └── truth/           Binary labels: 5,088 training / 300 validation rows
    ├── report.template.tex  LaTeX report skeleton for questions 1–9
    └── extract_intrep.py    Optional Qwen feature extraction; requires CUDA
```

Each dataset has `train.csv`, `valid.csv`, and matching `.npy` features for layers **11, 23, 35**. Features have 2,560 columns and align with CSV rows. Preserve these inputs. Use `lab1/output/pNN/` for phase-specific experiment artifacts and `lab1/submission/` for selected final deliverables when needed.

## 3. Work order and time budget

Estimate for your strong mathematical background and developing Python skills, using supplied features:

| Stage | Focus | Focused time |
| --- | --- | --- |
| Read and prepare | Handouts, code, root `.venv`, dependencies | 2–3 h |
| Implement and check | NumPy gradient descent, L1/L2, stable logistic probabilities, toy checks | 4–6 h |
| Run experiments | Establish both baselines; compare layers and regularization; collect plots and evidence | 6–10 h |
| Report and package | Answer all nine questions, verify exports, rehearse the live demonstration | 6–9 h |
| **Total** | **About 5–7 sessions of 3–4 hours** | **18–28 h** |

This is a planning estimate, not a measured runtime. Reserve another **4–8 hours** for debugging or unfamiliar plotting/LaTeX tools. Completing HW1 separately and optional GPU work are excluded.

Prioritize a working baseline, then the report evidence and truth-classification experiments: truth carries more model-performance weight than coordinates. Core training uses NumPy/pandas on supplied features; no LLM download or GPU is needed. Reuse the repository's root `.venv`; scikit-learn supports comparisons and matplotlib supports plots.

**Finish line:** handwritten model training with gradient descent and both regularizers; two `.npz` weight files plus chosen layer numbers; a PDF report answering questions 1–9; runnable code and a live demonstration. The handout allows library-trained final weights, but the handwritten implementation is still required. Submission platform details remain pending in the handout.
