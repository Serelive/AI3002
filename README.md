# AI3002 — Foundations of Artificial Intelligence and Machine Learning

Fall 2026 course workspace. Active work is [Lab 1: linear probes](assignments/labs/lab1/README.md); continue on the 107 platform using the [HPC handoff](docs/HPC.md). Persistent working instructions are in [AGENTS.md](AGENTS.md).

## Environment

Use one root Python environment and the committed uv lock file:

```bash
uv sync --locked
.venv/bin/python -c "import course_utils, numpy, pandas, sklearn, matplotlib"
```

Python 3.11 or later is required. Local checks use Python 3.14.4. Recreate `.venv` on each machine, or use the documented `ai26` Conda option on the cluster. See [PyCharm setup](docs/PYCHARM.md) for local development and [Slurm setup and jobs](docs/HPC.md) for login/compute-node use.

## Workspace

| Path | Purpose |
| --- | --- |
| `assignments/labs/lab1/scr` | Models, training scripts, focused tests, and working notebook |
| `assignments/labs/lab1/docs/` | Active guides, input provenance, and current review |
| `assignments/labs/lab1/output/` | Local experiment results and Slurm logs; ignored |
| `assignments/labs/lab1/report/` | Report source |
| `scripts/slurm/` | Batch launcher |
| `src/course_utils/` | Importable shared package |
| `materials/`, `data/` | Local originals and shared data, with tracked indexes |
| `archive/` | Retained tutorials, practice notebook, and resolved reviews |
| `scratch/` | Disposable local work and transfer bundles; ignored |

The lab's immutable inputs live in `main/datasets/` and are transferred separately; see [input recovery](assignments/labs/lab1/docs/INPUTS.md). Existing legacy outputs under `main/output/` are preserved and ignored. Selected final deliverables belong in the assignment's `submission/` directory.

## Status and deadlines

| Work | Status | Deadline |
| --- | --- | --- |
| [Lab 1](assignments/labs/lab1/README.md) | Models and export fixes implemented; Task 2 experiments available; Task 3 tuning and report/submission selection remain | October 21, 2026 in current course repository |

The [current course repository](https://github.com/ChangshuoShen/USTC-AI3002-26fall/) still lists October 21 as of October 20; the supplied starter README says October 31. Use October 21 for planning and resolve the discrepancy through class notices.

User-supplied grading context: individual project 60%, team project 40%, possible 2-point useful-suggestion extra credit. Prioritize reproducible baselines, validation-based selection, and final deliverables; verify how extra credit is applied before calculating grades.

## Git and handoff

The configured remote is `git@github.com:Serelive/AI3002.git`; active development is on `feat/lab1`. See [version control and push preparation](docs/VERSION_CONTROL.md). Generated files, environments, datasets, and original handouts are excluded from new commits. Older history still contains supplied inputs; review the history note before publishing this branch.

Archived learning material is indexed in [archive/README.md](archive/README.md). The repository was initialized on September 9, 2026 and adapted for the HPC handoff on October 20.
