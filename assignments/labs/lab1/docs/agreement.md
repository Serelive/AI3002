# Lab 1 working agreement

## Scope and stages

`lab1` means `assignments/labs/lab1`. Task numbers ignore capitalization and spacing: `task1` and `Task 1` mean the same thing.

- **Task 1:** implement linear and logistic regression.
- **Task 2:** predict geographic coordinates.
- **Task 3:** classify sentence truth.

Use `pNN` for phases and `iNN` for increments, with two-digit numbers (e.g., `p01-i02`). These are lightweight progress markers, not rigid stages.

## Files in `scr/`

Every newly created or added file in `scr/` must use `pNN_<description>.<extension>`, where `NN` is the owning phase's two-digit number. This applies to Python scripts, notebooks, and other new files. Use descriptive names, for example `p02_check_world.py`, `p02_search_world.py`, and `p02_scaffold.ipynb`.

Keep existing supplied/shared files such as `model.py`, `train1.py`, and `train23.py` at their established paths when editing them; this rule governs new files, not a blanket rename of existing files. New phase-specific helpers must use the prefix even when they import these shared modules. Keep generated artifacts in `output/pNN/`, not `scr/`.

## Documentation

Keep lab-wide documents in `docs/` and all new phase-specific documents in `docs/pNN/`, including guides, checklists, plans, and increment reviews. A phase prefix in the filename does not replace the directory requirement. For example, the Task 2 checklist belongs at `docs/p02/p02_checklist_main.md`, not directly in `docs/`. Do not create increment folders. Update relative links when moving a document.

Name documents `[<scope>_]<type>[-rNN][_<keywords>].md`:

- **Scope:** omit for lab-wide documents; use `pNN` for a phase or `pNN-iNN` for an increment.
- **Type:** `plan`, `reference`, `roadmap`, `agreement`, `guide`, `checklist`, or `review`. Use `review` only for an independent review.
- **Keywords:** optional; separate multiple words with hyphens.
- **Review depth:** omit for the original document; use `-r01` for its review, `-r02` for a review of that review, and so on. Retain the original scope, type, and keywords to identify the document being reviewed. This suffix is not a version number.

Examples: `reference_quickguide.md`, `p01-i02_plan.md`, and `p01_review-r01_model.md` (a review of `p01_review_model.md`).

## Version control

Use Git for version history; keep filenames stable. After creating or meaningfully editing a document, check it, stage the relevant changes, and commit them together. Respect repository ignore rules and leave unrelated changes out.

## Generated output

Place phase-owned artifacts under `lab1/output/pNN/`: Task 1 figures/tables in `p01`, world training and comparison results in `p02`, and truth results in `p03`. Put run directories, logs, extracted features, and selected candidates beneath the owning phase. Shared Slurm checks may use `output/shared/slurm/` because they cover multiple phases. Final chosen deliverables belong in `submission/`.

Training defaults follow this mapping; explicit `--output_dir` remains available for temporary checks and custom run subdirectories. For coursework runs, choose a directory inside the owning phase. Keep supplied datasets unchanged. Legacy files retain their original locations until deliberately migrated or deleted; consult the [output audit](../../../../docs/LAB1_OUTPUT_AUDIT.md) first.
