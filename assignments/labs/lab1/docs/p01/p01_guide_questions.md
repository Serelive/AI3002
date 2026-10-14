# Phase 1 — Guide to questions 1–3

**Yes: use separate experiment scripts**, importing your classes from `model.py`. This is a suggested organization, not a submission requirement. Keep model logic in `main/model.py`, save figures/tables in `output/p01/`, and write the explanations in your report under `report/`. Paths below are relative to `lab1`.

## Question 1 — L1/L2 coefficient paths

Suggested script: `main/question1_paths.py`.

1. Read slides pp. 42 and 48 to identify the plots to reproduce; consult `docs/instruction.pdf` §2.1 for the question.
2. Construct or select a small regression dataset. Record its source or generation rule and random seed. Use comparable feature scales.
3. Fit models across a logarithmic grid of regularization strengths: vary L1 with L2 zero, then L2 with L1 zero. Keep the dataset and preprocessing fixed.
4. Plot each fitted coefficient against regularization strength. Check convergence: fixed-step L1 gradient descent may oscillate near zero, so tiny nonzero coefficients are not necessarily a conceptual error.
5. Save two plots and explain the data source and the difference between the paths.

## Question 2 — Why thresholding small L2 coefficients can fail

Suggested script: `main/question2_selection.py`.

1. Read slide p. 44. Construct a regression example with known relevant and irrelevant features; correlated relevant features are a useful starting point.
2. Split training and validation data with a fixed seed. Fit any scaling on training data only.
3. Compare L2 predictions before and after setting small coefficients to zero, and compare with L1. State the threshold and regularization strengths; examine a small range rather than selecting only a favorable case.
4. Record retained features and validation MSE. Explain what the example demonstrates: small L2 coefficients need not identify dispensable features. Do not claim L1 always performs better.

**Output:** a compact comparison table and an explanation supported by the observed results.

## Question 3 — Compare with scikit-learn

Suggested script: `main/question3_comparison.py`; this answer can wait until Tasks 2–3 are complete.

1. Fit your models and scikit-learn models on identical training data and preprocessing.
2. Match intercept treatment, objective normalization, and regularization strength; equal numerical penalty settings do not necessarily mean equal objectives.
3. Compare validation MSE for regression and accuracy plus log loss for classification. Check convergence before interpreting differences.
4. Report a small metric table and a brief explanation of any differences.

For each script, record the seed, settings, and run command. Example from the **course repository root**, once the script exists:

```bash
.venv/bin/python assignments/labs/lab1/main/question1_paths.py
```

These scripts are proposed, not yet created or executed. The referenced slides must be consulted before claiming their figures have been reproduced.
