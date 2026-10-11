# AI3002 — Foundations of Artificial Intelligence and Machine Learning

Term: Fall 2026. This is one Python course workspace for multiple assignments and project deliverables.

Open this repository root in PyCharm, select `.venv/bin/python`, and normally start Codex from the same root. The persistent course instructions are in `AGENTS.md`.

## Environment

Linux; Python; PyCharm; Git; Codex CLI or desktop. Setup created one root virtual environment and installed no third-party packages. Add only packages required by an actual project. `pyproject.toml` defines the reusable `src/` package layout; add a lock file when a dependency-locking workflow is selected.

Quick check from the repository root:

```bash
source .venv/bin/activate
python --version
PYTHONPATH=src python -c "import course_utils"
```

See `docs/PYCHARM.md` for IDE setup.

## Layout

```text
AI3002/
  AGENTS.md
  README.md
  pyproject.toml
  .venv/                    # Root interpreter; ignored
  materials/                # Read-only instructor originals; ignored
  assignments/              # One Axx-topic folder per actual assignment
  src/course_utils/         # Shared reusable Python code
  data/shared/{raw,processed}/
  tests/                    # Focused shared-code checks when needed
  scripts/                  # Shared workflow helpers when needed
  scratch/                  # Disposable experiments; ignored
  archive/                  # Retained inactive work
  templates/assignment/README.md
  docs/{PYCHARM,VERSION_CONTROL}.md
```

Create only the project or assignment subdirectories that are needed. They may use `src/course_utils/` but must not import code from one another. Keep code and documentation relocatable with project-relative paths.

## Assignments and projects

Lab 1 has been set up; no final submission has been selected.

| Identifier | Topic | Owner | Status | Due |
| --- | --- | --- | --- | --- |
| Lab 1 | [Linear probes](assignments/labs/lab1/README.md) | Individual | Orientation complete; implementation pending | See assignment README |

## Course priorities

User-supplied grading context: individual project 60%; team project 40%; possible 2-point extra credit for useful suggestions. Secure reproducible baselines before tuning, separate training/validation/test roles, and make team interfaces and ownership explicit. Verify the extra-credit scale before grade calculations. Current instructor instructions take precedence.

## Version control

The repository has an initial checkpoint on `main`. `docs/VERSION_CONTROL.md` explains local commits and later publication to a separate private GitHub repository. Setup created no remote and uploaded nothing.

See [the practical Git lecture](docs/GIT_COURSEWORK_LECTURE.md) for worked examples. Supplied Lab 1 datasets, archives, instructor PDFs, local Codex configuration, and report build products are ignored. [Input recovery instructions](assignments/labs/lab1/docs/INPUTS.md) and checksums are tracked; keep a separate backup of the inputs. Existing history still contains previously committed materials.

## Setup provenance

Initialized on 2026-09-09 from the supplied Linux/Python course prompt. `AGENTS.md` is a byte-for-byte copy of that prompt.
