# Using Git for a course programming repository

This lecture uses AI3002 repository observations from October 10, 2026. It supplements `VERSION_CONTROL.md`. The goal is simple: preserve your work, understand each checkpoint, and reproduce an assignment without collecting every file on your computer in Git. A single main branch and deliberate local commits are sufficient for most individual coursework.

## 1. Should a data file be ignored?

Not necessarily. A small, stable, permitted dataset can reasonably be tracked, especially if it is a test fixture or data you created. File purpose, size, provenance, and the repository's policy matter more than the `.csv` extension.

Here, `../../assignments/labs/lab1/scr` is tracked and unchanged. It occupies approximately 324 KiB on disk. Its size alone is not a compelling reason to exclude it. However, this repository's existing policy keeps instructor inputs and raw datasets outside ordinary commits. Ignoring the supplied Lab 1 datasets would make the implementation consistent with that policy.

The decision must include a way to recover the inputs: document the source, archive version or checksum, destination directory, and any extraction steps. Keep a separate local backup if the source might disappear. An ignored file is not backed up by Git.

Do not add a blanket `*.csv` rule: it could also hide a small results table you intentionally want to preserve.

## 2. Understand the three places Git works with

Think of Git as managing three versions of your work:

1. **Working tree:** files currently on disk, including your unsaved-to-Git edits.
2. **Index, or staging area:** the exact content selected for the next commit.
3. **Commit history:** saved snapshots that you can inspect and recover.

`git add` copies current file content into the index. It does not commit it. If you edit the file afterward, that later edit is not automatically staged. `git commit` records the index, not everything currently on disk.

There are also three useful file categories:

| Category | Meaning |
| --- | --- |
| Tracked | Git already has an index entry for the file. Changes are reported. |
| Untracked | The file exists, but is not in the index and is not excluded by an ignore rule. |
| Ignored | An untracked file is excluded by an ignore rule and normally omitted from status output. |

**An ignore rule does not stop tracking an already tracked file.** Adding `train.csv` to `.gitignore` would not remove its index entry or its old committed versions.

Run these read-only commands from the repository root:

```bash
git status --short
git diff
git diff --cached
git ls-files -- assignments/labs/lab1/scr/datasets/truth/train.csv
git check-ignore -v --no-index -- assignments/labs/lab1/scr/datasets/truth/train.csv
```

`git diff` compares working files with the index; `git diff --cached` compares the index with the latest commit. `git ls-files` checks tracking. `git check-ignore -v --no-index` tests ignore rules even for a tracked path and identifies the matching rule, if any. Ordinary `git check-ignore` skips tracked files, so its silence alone does not prove that no pattern matches.

## 3. What looks untidy in this repository?

“Non-standard” does not mean invalid Git. These are concrete policy mismatches, redundant artifacts, or unresolved choices. They require different responses.

| Observed artifact or state | Interpretation and proportionate action |
| --- | --- |
| Tracked CSV and `.npy` inputs in `main/datasets/` | Conflicts with the documented local-input policy. Keep them locally and document recovery before stopping tracking. |
| Three `truth/train.layer*.npy` files, about 25 MiB each | Large binary inputs make repository storage and transfers heavier; ordinary text diffs do not explain their changes. Prefer documented local inputs for this course. These sizes are approximate disk usage, not measured Git pack sizes. |
| Tracked `backups/LAB1.zip`, about 69 MiB | An original archive may be useful locally, but tracking it alongside extracted materials adds bulk. Keep a separate backup and a provenance record. |
| `backups/HW1-26.pdf` and the homework PDF; `backups/LAB1.pdf` and `docs/instruction.pdf` | Each pair has identical SHA-256 hashes. They are duplicate content. Git may deduplicate identical blobs, so two paths do not necessarily double storage, but they still create ambiguity about the authoritative copy. |
| Untracked report `.aux`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, and `.xdv` files | LaTeX build intermediates. Ignore them within the report directory; they are not report source. |
| Untracked `report.template.pdf` | A compiled report needs a purpose-based decision. Ignore routine builds, but deliberately retain a selected final PDF in `submission/` if needed. Do not globally ignore every PDF. |
| Modified `pyproject.toml` and untracked `uv.lock` | If uv is the selected dependency workflow, review and commit the lock file with the corresponding dependency change. A lock file is a reproducibility artifact, unlike the disposable environment directory. Its presence alone does not prove installation succeeded. |
| Untracked `.codex/` | Its tracking policy is undecided. Inspect configuration before choosing: portable project settings can be tracked; personal paths, machine-specific settings, and secrets should stay local. The directory name alone is insufficient. |
| Root README still says no deliverable has been created and shows an empty assignment index | Documentation has fallen behind the Lab 1 workspace. Updating the index and environment instructions would make the repository easier to understand. |

There are also normal work-in-progress states. At inspection, some changes were staged and others were unstaged. Two documentation renames were staged. Neither is evidence of misuse. In short status output, the first column describes the index and the second describes the working tree:

```text
 M file.py       modified on disk, not staged
M  file.py       modification staged
AM notes.md     added to the index, then edited again
?? new.txt      untracked
!! .venv/       ignored (shown with --ignored)
```

The observed `AM` state for Lab 1's `docs/agreement.md` means a commit would contain its staged version, not all current edits. Inspect both diffs before deciding whether to stage the newer content. A staged rename is an ordinary change; Git detects renames by comparing content.

## 4. Why the existing ignore rules missed Lab 1

The root `.gitignore` contains patterns such as:

```gitignore
/assignments/*/data/**
/assignments/*/output/**
```

These assume a layout like `assignments/A01-topic/data/`. A single `*` does not cross directory separators. The actual dataset lives under `../../assignments/labs/lab1/scr`: both the depth and directory name differ. The output rule also misses `assignments/labs/lab1/output/`.

Likewise, ignoring `/materials/**` does not ignore instructor PDFs copied into assignment `docs/` or `backups/` directories. Ignore patterns describe paths; they do not understand that a file is “course material.”

For a small course repository, explicit paths are easy to inspect. A possible addition to the root `.gitignore` is:

```gitignore
# Lab 1 supplied inputs and local archive copies
/assignments/labs/lab1/main/datasets/
/assignments/labs/lab1/backups/

# Lab 1 generated experiment output
/assignments/labs/lab1/output/

# Lab 1 report build intermediates
/assignments/labs/lab1/report/*.aux
/assignments/labs/lab1/report/*.fdb_latexmk
/assignments/labs/lab1/report/*.fls
/assignments/labs/lab1/report/*.log
/assignments/labs/lab1/report/*.out
/assignments/labs/lab1/report/*.xdv
/assignments/labs/lab1/report/*.synctex.gz
```

These are proposed rules, not changes applied by this lecture. Keep input provenance in the assignment README, outside the ignored dataset directory. Decide separately how to retain instructor handouts and final PDFs; the sample rules do not resolve every existing policy mismatch.

## 5. Stop tracking without deleting local data

First verify that you can restore the inputs and inspect any pending changes to them. After adding the intended ignore rules, the following would remove these paths from the index while retaining their working-tree files:

```bash
git rm -r --cached -- assignments/labs/lab1/scr/datasets/ assignments/labs/lab1/backups/
git add -- .gitignore
git diff --cached --stat
git diff --cached --name-status
git status --short
```

The staged deletions mean “absent from the next Git snapshot,” not “deleted from this computer.” Do not omit `--cached`. If Git refuses because index and working-tree versions differ, inspect the differences rather than forcing the operation.

Review the entire index before committing: this repository already has unrelated staged work, and `git commit` would include it too. Finish that checkpoint first or unstage specific unrelated paths with `git restore --staged -- PATH`, which retains their working-tree content.

After the cleanup commit, a fresh clone will need the documented input-restoration procedure. Old commits still contain the data, and ordinary removal does not shrink existing history. Rewriting history is unnecessary for this routine course cleanup. Also, removing a file from the latest snapshot does not remove it from history that a later push can transmit.

None of these cleanup commands were executed in preparing this note.

## 6. A small, repeatable working routine

Before starting, run `git status` to see unfinished work. After making one coherent change, run the relevant script or check, inspect the diff, and stage explicit paths. For example, after actually implementing and checking a model change:

```bash
git diff -- assignments/labs/lab1/scr/model.py
git add -- assignments/labs/lab1/scr/model.py
git diff --cached
git status --short
git commit -m "Implement Lab 1 linear model"
```

This is an illustrative workflow, not a claim that the model is implemented or validated. Include the assignment README when it records related run instructions or results. Review all staged content before the commit. Avoid casually using `git add .` while the workspace contains unreviewed data and report builds.

A useful commit represents one understandable checkpoint: dependency setup, an implementation, a documented experiment, or a tracking cleanup. There is no need for a prescribed commit-prefix system. A clear message is enough.

For Python, track `pyproject.toml` and the chosen lock file; keep `.venv/` ignored. The manifest declares dependencies, the lock records a resolved dependency set, and `.venv/` contains the local installation. Record the command used to recreate that installation and the required inputs in the README. Do not assume a lock file makes external datasets available.

For experiments, retain code, configurations, random seeds, concise metrics, and exact run commands. Keep bulk intermediate output local. Copy deliberately selected report and model deliverables into `submission/` when preparing a submission. Git tracking, a GitHub push, and uploading an assignment to the course platform are separate actions.

Use read-only commands to investigate mistakes first:

```bash
git log --oneline -5
git diff --cached
git show HEAD:assignments/labs/lab1/scr/model.py
```

`git restore --staged -- PATH` undoes staging while preserving edits. In contrast, `git restore -- PATH` can discard unstaged edits. Avoid `git reset --hard` or `git clean` as routine tidying tools; uncommitted and ignored work may have no recoverable Git copy.

## 7. A practical order for later cleanup

1. Review the existing staged and unstaged changes so their intended checkpoints remain intact.
2. Document where Lab 1 inputs came from and verify the local backup or recovery procedure.
3. Add narrowly scoped ignore rules and stop tracking only the selected local inputs and archives.
4. Resolve the dependency manifest and lock file together, and update stale README setup and assignment information.
5. Build and review the report, then select final deliverables deliberately.

No branch policy, pull-request template, automated CI system, or large-data service is required to achieve this. The essential check is whether another copy of your repository, together with documented inputs and environment setup, can reproduce the work you intend to submit.
