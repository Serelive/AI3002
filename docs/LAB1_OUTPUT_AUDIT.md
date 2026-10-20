# Lab 1 output layout and existing-artifact audit

Audited October 20, 2026. Repository-relative paths are used below. The canonical Lab 1 source directory is currently `assignments/labs/lab1/scr/`.

## Adopted layout

Use **`assignments/labs/lab1/output/pNN/` for phase-owned results**, including model files, plots, tables, extracted features, run records, and logs. Keep meaningful subdirectories such as `comparison/<batch>/<configuration>/` so separate experiments remain identifiable.

| Producer | Default destination relative to Lab 1 |
| --- | --- |
| Phase 1 figures/tables, when produced | `output/p01/` |
| `scr/train23.py world ...` | `output/p02/` |
| `scr/train23.py truth ...` | `output/p03/` |
| `scr/p02_comparison.py` | `output/p02/comparison/<timestamp>/` |
| `scr/extract_intrep.py --token-selection country` | `output/p02/features/` |
| `scr/extract_intrep.py --token-selection last` | `output/p03/features/` |
| Slurm world/comparison jobs | `output/p02/slurm/job-JOBID/` |
| Slurm truth jobs | `output/p03/slurm/job-JOBID/` |
| Slurm checks spanning multiple phases | `output/shared/slurm/job-JOBID/` |

`shared/` is the one explicit exception for work with no single owning phase. Put scheduler logs under the corresponding `slurm/logs/` directory, created before `sbatch`. The launcher now points to `scr/` instead of the removed `main/` directory. See [HPC.md](HPC.md) for submission commands.

Explicit `--output_dir` still supports temporary tests and custom run directories. For coursework, keep overrides beneath the owning phase. Feature extraction now writes generated arrays outside the immutable supplied dataset directory; copy or reference them deliberately when preparing a later training dataset. Final selected submission artifacts still belong in `submission/`.

## Existing files: what can be identified?

The [archive inventory](LAB1_OUTPUT_INVENTORY.csv) lists **all 410 `.npz` files** found in Lab 1's canonical and legacy output locations, plus the adjacent legacy `assignments/labs/output/`. It records file hashes, array-content hashes, schema checks, and provenance evidence. Array-content hashes allow equivalent weights to be matched even when archive bytes differ.

Every inspected archive has finite weights/bias and the expected float64 shapes for either world or truth. Finite arrays establish usability at the format level; exact training provenance comes from the records below. Validation metrics were read from saved records, not recomputed.

### Keep: identifiable comparison batches

| Directory under `lab1/output/p02/comparison/` | Recorded runs | Selected configuration | Recorded validation MSE |
| --- | ---: | --- | ---: |
| `20261017-070517-087127` | 375 successful | layer 11; L1 0.1; L2 0.1; lr 0.0001; 10,000 updates | 176.64373815281513 |
| `20261017-153204-625946` | 27 successful | layer 11; L1 0.3; L2 0.3; lr 0.0001; 10,000 updates | 167.64679157934128 |

All 402 run archives have matching configuration/result settings. Each batch's `selected/world.npz` exactly matches its recorded source run's arrays, and the layer file agrees. Keep these batches and their selected-model records. They identify the numerical settings and scores; the old metadata does not independently establish the exact code revision or package environment.

The three standalone text logs already in `output/p02/` are identifiable as the starting checks, six-pair input check, and interrupted early comparison transcript. Keep them as historical evidence; they are not additional selected models.

### Legacy outputs: one matched file and five incomplete records

| Existing path | Identification | Recommended handling |
| --- | --- | --- |
| `assignments/labs/lab1/output/world/world_layer11.npz` | Arrays exactly match initial-batch run `0027_layer11_l1-0.0001_l2-1e-05_lr-1e-06` | Redundant parameter copy; keep the recorded source run if later deleting this file. |
| `assignments/labs/lab1/output/world/world_layer23.npz` | World/layer 23 inferred from name and schema; no matching recorded parameter arrays | Keep pending your decision; candidate for deletion if no external settings record exists. |
| `assignments/labs/lab1/output/world/world_layer35.npz` | World/layer 35 inferred; no matching recorded parameter arrays | Same. |
| `assignments/labs/lab1/output/truth/truth_layer11.npz` | Truth/layer 11 inferred; no accompanying training settings | Same; do not confuse it with the other truth archive. |
| `assignments/labs/lab1/scr/output/truth/truth_layer11.npz` | Truth/layer 11 inferred; no accompanying training settings | Same. |
| `assignments/labs/output/world/world_layer11.npz` | World/layer 11 inferred; outside the Lab 1 tree and no matching recorded arrays | Same. |

“Partial identity” means the task/layer can be inferred but the originating experiment cannot be reconstructed confidently. File timestamps and plausible weights are insufficient to recover learning rates, penalties, preprocessing, or iteration counts. If an external experiment record resolves a file, move it to `output/p02/legacy/<source-name>/` or `output/p03/legacy/<source-name>/` with that record. Use distinct subdirectories to preserve same-named archives.

**No existing output was moved, overwritten, or deleted.** The five incomplete records remain available for your later deletion decision. The code refactor controls future output placement; this inventory preserves the original paths for identification.

## Verification and reproduction

Executed locally:

```bash
bash -n scripts/slurm/lab1.sbatch
OPENBLAS_NUM_THREADS=1 .venv/bin/python tests/test_slurm_launcher.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python tests/test_lab1_output_paths.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python assignments/labs/lab1/scr/p03_test_iteration.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python assignments/labs/lab1/scr/p02_test_comparison.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python assignments/labs/lab1/scr/p01_test_linear-regression.py
```

All 18 test methods passed. Tests cover task-to-phase defaults, explicit overrides, extraction routing without a GPU, overwrite protection, launcher paths/threads, and existing training/export behavior. The extraction fixture was corrected to satisfy the existing country-token input format before its successful rerun. No LLM extraction or Slurm job was launched. On 107, run numerical checks through an allocated compute job and keep its checkout stable while running.

The inventory is a snapshot, not a live database. Its `file_sha256` column can be used to verify that the inspected files are unchanged before any later cleanup. Outputs remain ignored by Git; this audit, inventory, code, and documentation are tracked.
