# Lab 1 working agreement

## Scope and stages

`lab1` means `assignments/labs/lab1`. Task numbers ignore capitalization and spacing: `task1` and `Task 1` mean the same thing.

- **Task 1:** implement linear and logistic regression.
- **Task 2:** predict geographic coordinates.
- **Task 3:** classify sentence truth.

Use `pNN` for phases and `iNN` for increments, with two-digit numbers (e.g., `p01-i02`). These are lightweight progress markers, not rigid stages.

## Documentation

Keep lab-wide documents in `docs/` and phase-specific documents in `docs/pNN/`. Do not create increment folders.

Name documents `[<scope>_]<type>[-rNN][_<keywords>].md`:

- **Scope:** omit for lab-wide documents; use `pNN` for a phase or `pNN-iNN` for an increment.
- **Type:** `plan`, `reference`, `roadmap`, `agreement`, or `review`. Use `review` only for an independent review.
- **Keywords:** optional; separate multiple words with hyphens.
- **Review depth:** omit for the original document; use `-r01` for its review, `-r02` for a review of that review, and so on. Retain the original scope, type, and keywords to identify the document being reviewed. This suffix is not a version number.

Examples: `reference_quickguide.md`, `p01-i02_plan.md`, and `p01_review-r01_model.md` (a review of `p01_review_model.md`).

## Version control

Use Git for version history; keep filenames stable. After creating or meaningfully editing a document, check it, stage the relevant changes, and commit them together. Respect repository ignore rules and leave unrelated changes out.
