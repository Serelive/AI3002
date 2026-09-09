# AI3002 — Foundations of Artificial Intelligence and Machine Learning: local project instructions

## Communication and English learning

Respond in English unless the user explicitly requests Chinese for the response or a deliverable. Be instructive, strict about correctness, and respectful. Point out errors directly and explain how to fix them; do not replace criticism with praise. Use clear, concise language and scale detail to the question.
Append a short **English revision** section to every response. Review the user's English prose, offer a natural correction that preserves meaning, and explain at most one or two useful changes. For long prompts, revise the relevant sentences without repeating technical specifications or code. If no English prose needs correction, say so briefly. Keep language feedback after the substantive answer and outside submission artifacts unless requested.

## Purpose and working approach

This repository is one course-level computational workspace containing multiple assignments. The primary goal is a higher grade within limited time; the secondary goal is stronger implementation skills and understanding.

The learner has completed Mathematical Analysis, Real Analysis, Linear Algebra, Probability, Statistics, Stochastic Processes, R, Data Structures, and Foundations of Algorithms. Their theoretical background is stronger than their computational knowledge and implementation skills. Use this background without assuming mastery; explain implementation details explicitly.

For a request to implement or fix something, carry it through to a usable, checked result within the requested scope. For a conceptual question, answer directly without changing files unnecessarily. Explain the key equation-to-code connections and unfamiliar constructs concisely. Ask only when missing information materially affects correctness or scope; otherwise state reasonable assumptions and proceed.

## Repository contract

Use the existing structure and create directories only when needed:

- Root README.md: course identity, environment and setup, assignment index, known status and deadlines.
- Root AGENTS.md: persistent course-wide agent instructions; inspect any applicable nested instructions too.
- materials/: instructor-provided syllabus, handouts, references, and starter materials; treat originals as read-only.
- assignments/Axx-topic/: assignment-local README.md, prompt/, data/, work/, output/, and submission/ as needed. A small assignment may keep its script and report directly in the assignment folder.
- data/shared/: course-wide data; separate immutable raw inputs from reproducible processed data where needed.
- tests/ and scripts/: useful shared validation and workflow helpers.
- scratch/: disposable experiments; archive/: inactive retained work.

An assignment may use shared course resources but must not import or source code from another assignment. Promote a small reusable abstraction to the course-wide code directory only when reuse justifies it. Do not build speculative infrastructure.
Never overwrite raw datasets or instructor originals; copy starter code to the assignment workspace before editing it. Keep generated artifacts in the assignment's output/ and deliberately selected final deliverables in submission/. Keep scratch work out of the repository root. Respect existing user changes.
Use relocatable project-relative paths. Ignore environments, caches, and transient outputs as appropriate. Keep large/private materials locally if needed without automatically adding them to Git; record provenance in a small index where useful.

## Assignment workflow and verification

1. Identify the active assignment from the request and context. Read the root README, applicable instructions, assignment README, original prompt, rubric, and relevant files before editing. If the assignment cannot be identified, ask for its identifier while doing any useful independent inspection.
2. Establish required inputs, allowed packages/methods, deliverable names and formats, and known deadlines. Prefer the latest applicable instructor guidance over old references or these defaults. Do not invent grading rules, missing data, results, or syllabus coverage.
3. Inspect the actual environment and existing code. Make the smallest coherent implementation that meets the task. Explain the approach briefly when the work is substantial.
4. Validate proportionately: run the relevant script or report in a fresh process when feasible, check dimensions and edge cases, and compare numerical results against known cases where useful. Add focused tests for reusable or error-prone logic; do not add a testing framework merely for a small assignment.
5. Record dependencies, random seeds for stochastic work, inputs, and exact reproduction commands. Avoid reliance on an interactive session's hidden state. Inspect important plots and rendered reports when tools permit. Clearly distinguish executed checks from proposed checks and report blockers honestly.
6. Update the assignment README with the task, inputs, main files, reproduction steps, selected deliverables, assumptions, and meaningful status changes. When preparing a submission, check it against the prompt and rubric; account for any shared code it needs in the required packaging. Preparing submission/ does not itself authorize uploading the work.

In the final response, state what changed, the relevant files, how to reproduce it, what was verified, and any remaining issue. Keep explanations educational but proportional to the task. Follow any supplied assessment-specific collaboration or tool-use rules.

## Cloud and local handoff

The repository is the source of truth for executable code, dependencies, outputs, and submission artifacts. Do not assume access to the paired cloud project's conversations or uploads, or automatic synchronization. If essential context is missing, request the relevant excerpt.
When a conceptual issue needs cloud discussion, provide a compact handoff containing the course and assignment, question, relevant equations or minimal code, observations, and uncertainty. Accept cloud suggestions as inputs to verify against the actual repository and assignment.

## Python environment

Use Python on Linux with Codex CLI and PyCharm. Open the course repository root in PyCharm and normally start Codex CLI there. Reuse one root .venv and the repository's dependency workflow, normally pyproject.toml with an appropriate lock file when used. Do not create per-assignment environments unless incompatible requirements justify an exception.
Put genuinely shared code in src/course_utils/ and configure its importability through the existing project setup; avoid ad hoc sys.path edits and imports across assignments. Use pathlib and project-relative paths, and give Linux shell commands using the configured interpreter. Prefer readable, explicit Python and only the packages needed by the assignment. Introduce numerical or ML libraries according to the actual course requirements rather than assuming a framework. Do not assume a GPU is available.

## Course-specific priorities

User-supplied grading context: Individual project 60%; team project 40%; extra credit of 2 points for useful suggestions. The scale and application of the extra credit are not specified; verify before calculating a final grade.

Organize study around project deliverables, evaluation criteria, deadlines, and reproducible evidence. Establish the individual-project baseline early and plan clear team interfaces and responsibilities. Do not invent an exam preparation requirement. Consider useful-suggestion extra credit only after core deliverables are secure.

Establish a simple reproducible baseline before tuning. Keep training, validation, and test roles separate, fit preprocessing only on allowed training data, and avoid test-set-driven model selection. Record configurations, seeds, metrics, and relevant runtime. For team work, make interfaces and ownership explicit and preserve teammates' changes. Treat earlier-semester code as reference material, not the current assignment specification.

These subject-specific checks apply when relevant to the assignment; they are not a verified list of course topics.

## Course references

Materials expected in the paired cloud project or provided locally: slides. Both 2025 links below are previous-semester references; the MIRA page is labeled AI3001.01, so do not assume its course identity, requirements, or grading match AI3002 this term.
The list does not establish that these resources are present locally. Read accessible current assignment materials first. Use course websites as references; reviews are anecdotal, and older-semester materials are not current specifications.

- [Previous-semester repository (Fall 2025)](https://github.com/ChangshuoShen/USTC-AI3002-25fall)
- [Related previous-semester course page (AI3001.01, Fall 2025)](https://miralab.ai/course/ml_2025fall/)
- [Relevant course reviews (anecdotal)](https://icourse.club/course/26106/)
- [Related Machine Learning A reviews (anecdotal)](https://icourse.club/course/25967/)
