# PyCharm setup

1. Open the repository root as one PyCharm project. Do not open each assignment as a separate project.
2. Select the existing interpreter at `.venv/bin/python`. If PyCharm does not detect the `src` layout from `pyproject.toml`, mark `src/` as **Sources Root**.
3. Set run-configuration working directories to the repository root. Code should use `pathlib` and project-relative paths rather than machine-specific absolute paths.
4. Keep the bundled Git integration enabled. PyCharm and command-line Git operate on the same local history.
5. Do not commit `.idea/`; it is intentionally ignored because most settings are machine-specific.

Install the recorded dependencies with `uv sync --locked` from the repository root. `pyproject.toml` and `uv.lock` define the environment used by the local scripts and HPC jobs.
