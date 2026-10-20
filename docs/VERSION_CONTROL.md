# Git and GitHub workflow

The local branch is `feat/lab1`, with `origin` configured as `git@github.com:Serelive/AI3002.git`. This HPC preparation does not push or change remote settings.

## Before publishing

Review the exact branch and diff:

```bash
git status --short --branch
git remote -v
git log -5 --oneline
git diff --check
git ls-files
```

The current tree excludes inputs, environments, and generated artifacts. Older commits reachable from this branch still contain `LAB1.zip` (about 68 MiB), dataset arrays, and instructor PDFs. A normal branch push includes those historical objects. Moving files into `archive/` retains them in Git; it is an organizational change, not history removal.

The October 20 audit found no blob at or above 100 MiB in local reachable history. The old lab archive and datasets remain a publication consideration. Preserve history if those contents belong in the destination repository; choose a clean snapshot branch or a deliberate history cleanup if they should stay local. No history rewrite has been performed. Remote visibility and existing remote history have not been checked.

When you have settled the history choice and are ready to publish, the command for this branch is:

```bash
git push -u origin feat/lab1
```

The command above is for you to run. Keep the repository private for coursework unless the course explicitly permits publication. Dataset recovery and transfer are described in [INPUTS.md](../assignments/labs/lab1/docs/INPUTS.md) and [HPC.md](HPC.md).

## Daily work across machines

Start with a clean working tree, then synchronize the same branch:

```bash
git pull --ff-only origin feat/lab1
# Edit and validate the task, then stage its specific files:
git add -- path/to/changed-file
git diff --cached
git commit -m "Describe the completed change"
```

Commit validated task changes automatically under the repository agreement. Review unrelated edits separately. Synchronize the cluster checkout between job batches so queued or running jobs use stable code. Transfer experiment results separately and deliberately select submission files.

The [archived Git tutorial](../archive/learning/GIT_COURSEWORK_LECTURE.md) covers Git concepts and worked examples.
