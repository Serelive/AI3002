# Git history cleanup review

Inspected October 20, 2026: `.git/filter-repo/analysis/`, current tracked files, rename records, and local branch tips. **Recommendation: remove historical input bundles and datasets from Git history; retain source code and archived documentation. No rewrite has been executed.**

## Remove from history

The accompanying [exact-path list](GIT_HISTORY_REMOVE_PATHS.txt) contains 26 historical paths:

| Group | Paths | Unique blobs | Reported compressed bytes, deduplicated |
| --- | ---: | ---: | ---: |
| `LAB1.zip` in old `main/` and `backups/` | 2 | 1 | 71,775,422 |
| Old `main/datasets/`: 12 feature arrays and 4 CSVs | 16 | 16 | 72,084,206 |
| Duplicated Lab 1 and HW1 instructor PDFs | 8 | 2 | 535,522 |
| **Total** | **26** | **19** | **144,395,150 (~137.7 MiB)** |

These are reproducible external inputs already excluded by `.gitignore`. Keep the physical inputs and separate backups: removing them from history removes Git as a recovery source. Follow [input recovery and checksums](../assignments/labs/lab1/docs/INPUTS.md).

All 26 paths are absent from the inspected tips of `feat/lab1`, `main`, and `origin/main`. The size report's aggregate is about 208.5 MiB, but repeated paths count the same ZIP/PDF blobs multiple times. `git count-objects -vH` currently reports 140.73 MiB of loose objects and no packfiles. The 137.7 MiB figure identifies the main storage burden, not a guaranteed disk-space saving after repacking.

## Keep

- `uv.lock`, source history under both old `main/` and current `scr/`, report sources, checksums, and input indexes.
- Archived reviews and learning notes: intentionally retained references, not abandoned binaries.
- The Matplotlib notebook: approximately 93 KiB compressed, shared across its old and archived paths. Removing it offers little benefit.
- Current output audit/inventory documents. The large experimental `.npz` files and reference-paper PDFs are ignored local artifacts, not history-cleanup targets in this analysis.

Do not filter the whole `main/`, `scr/`, or `archive/` directories. Many “old” paths are renames of useful files. Exact historical names are listed because filter-repo does not follow renames automatically. [Official filter-repo documentation](https://raw.githubusercontent.com/newren/git-filter-repo/main/Documentation/git-filter-repo.txt).

## Proposed command — run later, in a disposable mirror

Wait until queued/running 107 jobs no longer depend on a checkout you intend to replace. Back up ignored inputs and selected results separately. The bundle below preserves committed history and refs, not ignored files.

From the current repository root, after committing the review and path list, run these commands **only when ready to rewrite**. Choose unused sibling destination names if these already exist:

```bash
set -e
source_repo="$PWD"
git bundle create ../AI3002-before-filter.bundle --all
git bundle verify ../AI3002-before-filter.bundle
git clone --mirror --no-local "$source_repo" ../AI3002-history-clean.git
cd ../AI3002-history-clean.git

uv run --no-project --with git-filter-repo git-filter-repo \
  --invert-paths \
  --paths-from-file "$source_repo/docs/GIT_HISTORY_REMOVE_PATHS.txt"
```

The filter command removes only the listed paths from the mirror's reachable history. `--no-local` makes an independent clone; the fresh-clone check remains enabled because no `--force` is supplied. `uv run --no-project --with` supplies the tool without adding it to the course dependencies; it may download the package. [uv command reference](https://docs.astral.sh/uv/reference/cli/#uv-run).

Then inspect the rewritten mirror:

```bash
git fsck --full
git count-objects -vH
uv run --no-project --with git-filter-repo git-filter-repo --analyze
git log --all --format= --name-only -- \
  assignments/labs/lab1/main/datasets/ \
  assignments/labs/lab1/main/LAB1.zip \
  assignments/labs/lab1/backups/LAB1.zip
```

The last command should print nothing; use the new analysis to check all remaining PDF paths too. Compare `git ls-tree -r <branch>` between the original and rewritten `feat/lab1` and `main` tips: their tracked file contents should be unchanged, since the removal list contains no current files. Keep the mirror's `filter-repo/commit-map` to interpret historical commit IDs mentioned in experiment records.

This procedure leaves the original working repository, datasets, outputs, and GitHub untouched. Rewritten commits have new IDs; publishing them requires a separate coordinated force-update of the intended remote branches and replacement of old workstation/107 clones. Filter-repo normally removes `origin`. Inspect refs before reconnecting a remote; **do not blindly mirror-push** remote-tracking or backup refs. No push command is included in this proposal.

## Validation performed for this review

The path list was checked against the analysis and all three inspected branch tips: 26 exact paths, 19 unique blobs, and zero current tracked-file matches. The shell examples were syntax-checked without execution. No cloning, bundling, filtering, garbage collection, or remote update was performed.
