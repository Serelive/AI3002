# p03 guide and handoff: predict sentence truth

## Starting point and priorities

This guide is the entry point for the next Lab 1 conversation. Paths are relative to `assignments/labs/lab1/`; shell commands run from the course repository root. Read `docs/instruction.pdf` §2.3 and §3, then `scr/model.py` and `scr/train23.py`.

**Phase 2 is sufficiently implemented according to the learner.** Promising settings are layers 11 or 35, L1/L2 approximately 0.3–1.0, and learning rate around 0.0001. Further Phase 2 training and refinement will continue on the **107 platform**. Preserve its code and selected artifacts; focus this conversation on Task 3. These ranges describe Task 2 experiments, not starting hyperparameters to transfer unchanged to logistic regression.

Prioritize a working truth classifier, useful validation performance, and a valid export. The handout gives Task 3 more model-performance weight than Task 2. Use the supplied features and existing code; build only what is needed to run and compare experiments. A large testing or logging project is unnecessary.

## Required inputs and deliverables

Task 3 predicts a sentence's dataset label from one layer's Qwen3-4B-Base representation of the last token. Label 1 means true; 0 means false. The model outputs a probability; threshold it at 0.5 when computing classification accuracy.

Local files inspected for this handoff:

| Input under `scr/datasets/truth/` | Training | Validation |
| --- | --- | --- |
| CSV columns | `sentence`, `label` | `sentence`, `label` |
| Rows | 5,088 | 300 |
| Class counts | 2,544 per class | 150 per class |
| Features at each of layers 11, 23, 35 | `(5088, 2560)` | `(300, 2560)` |
| Stored feature dtype | float16 | float16 |

`load_split` already converts features and labels to float64. Preserve row alignment. Fit model parameters and any preprocessing on training data; use validation to choose settings.

The §2.3 submission interface is:

- One `.npz` containing `weights`: float64, shape **`(2560,)`**.
- `bias`: float64, shape **`()`**, a zero-dimensional array, not `(1,)`.
- One integer layer number in `[0, 35]`; the supplied choices are 11, 23, 35.

Final weights may be library-trained. The full lab still requires the handwritten gradient-descent implementation, runnable code, and report. Supplied-feature training needs no LLM download or GPU.

## Current code: reuse it, but fix the truth settings first

`LogisticRegressionModel` already implements full-batch gradient descent, L1/L2 gradients, an unregularized bias, and a stable sigmoid. `predict()` returns probabilities. Its handwritten gradient and behavior still need a focused review for this phase.

In `train23.main(args)`, the truth branch currently constructs:

```python
model = LogisticRegressionModel(train_x.shape[1])
```

Consequently, `--lr`, `--l1`, `--l2`, and `--max_iter` are parsed and validated but **not passed to the truth model**. It always uses constructor defaults. Fix this before timing, tuning, or claiming that different settings were compared:

```python
model = LogisticRegressionModel(
    train_x.shape[1], lr=args.lr, l1=args.l1,
    l2=args.l2, max_iter=args.max_iter,
)
```

The current truth branch consistently trains and predicts on raw features and exports raw-space parameters. Standardized arrays are computed earlier but unused by that branch. Keep a raw baseline, or deliberately adopt the same training-only standardization workflow used for Task 2. If standardizing, use transformed features for both fit and predict, then export `w_raw = w_z / scale` and `b_raw = b_z - mean @ w_raw`.

The runner already rejects non-finite final parameters/predictions and existing output archives. Pass a fresh `--output_dir` under `output/p03/`; the default routes world to `output/p02/` and truth to `output/p03/`. The earlier truth scale/export bugs described in historical reviews have been corrected. The ignored CLI settings above are the current issue.

## Short implementation plan

| Increment | Work | Completion evidence |
| --- | --- | --- |
| `p03-i00` | Wire the CLI settings into the truth model; briefly verify logistic gradient, probability range, and one small training example. | Requested settings reach the model; probabilities are finite and in `[0, 1]`; a small run works. |
| `p03-i01` | Run one supplied layer, starting with 11, with explicit settings and a stable learning rate. | Finite validation probabilities/accuracy and a saved archive. Record train accuracy too to spot overfitting. |
| `p03-i02` | Compare layers 11/23/35 and regularization using validation accuracy. | A small score table with actual settings, runtime, and the selected run. |
| `p03-i03` | Reload the selected weights on raw validation features and record its layer. | Export shapes/dtypes are correct; reloaded probabilities and accuracy match the selected run. |
| `p03-i04` | Write the two required report answers using observed data and comparison results. | Questions 8–9 have concise evidence-based answers. |

For the first run, fix L1 at zero and choose one L2 value. Use a short training pilot to choose a stable learning rate and an adequate iteration budget, then compare regularization. If calculating a curvature bound as in Task 2, logistic loss has smooth Hessian bound `A.T @ A / (4*N)`, plus the L2 term; the squared-error factor `2/N` is different. A stable sigmoid prevents exponential overflow but does not guarantee that an arbitrary learning rate trains well.

After the CLI fix, this is the command pattern; replace uppercase placeholders with the pilot's numeric settings:

```bash
.venv/bin/python assignments/labs/lab1/scr/train23.py truth 11 \
  --output_dir assignments/labs/lab1/output/p03/baseline-layer11 \
  --lr RATE --l1 0 --l2 PENALTY --max_iter ITERATIONS
```

The comparison runner for Task 2 is a useful structural reference, but it is hardcoded for world models and **minimizes MSE**. If a runner is needed, create `scr/p03_comparison.py`: use task `truth`, maximize accuracy, save each configuration separately, and export `truth.npz` with its layer. For equal accuracy, prefer a predeclared simple tie rule, such as lower validation binary cross-entropy. Keep settings, score, runtime, and the selected artifact; reuse the existing approach rather than designing new infrastructure.

A constant classifier scores 50% on this balanced validation set. Each corrected prediction changes accuracy by about 0.33 percentage points, so small differences may reflect only a few examples. Start with layers and L2, then add L1 if useful. Raw-feature and standardized-feature penalties have different meanings; label the preprocessing choice in the results.

## Final export check

With raw validation features `X`, recover probabilities from the loaded arrays:

```python
scores = X @ weights + bias
probabilities = np.exp(-np.logaddexp(0.0, -scores))
accuracy = np.mean((probabilities >= 0.5) == valid_y)
```

Confirm finite weights/bias, the required shapes/dtypes, and probability equality with the selected run using `np.allclose`. Keep one selected candidate and its layer under `output/p03/`, then copy the chosen files when preparing `submission/`. Retain an exact reproduction command and settings in the lab README. For a library classifier, also verify that its exported coefficients correspond to class 1.

## Report evidence to collect while training

**Question 8:** compare the training and validation sentences for actual distribution differences. Read examples from both splits, identify supported patterns in topic or wording, and explain how they influenced your approach. Class balance is already equal in both; do not present a label-proportion shift as the explanation. Save a few representative examples or counts rather than speculating about the hidden dataset construction.

**Question 9:** explain the chosen layer and regularization using the validation comparison. Preserve the table and settings now so the report does not require rerunning experiments. The related paper is locally available as `docs/papers/Marks2024.pdf`; consult it when interpretation needs support, after establishing the baseline.

## Handoff to the 107 platform or another conversation

Use the same repository revision, dependencies, and supplied inputs. Raw datasets and experiment outputs are ignored by Git: transfer them separately, using `docs/INPUTS.md` for recovery information. Bring back the selected `.npz`, layer, settings, metrics, and source revision. The platform's job commands and hardware have not been established in this conversation.

Suggested opening for the next conversation:

> Work on Lab 1 Task 3 using `docs/p03/p03_guide_main.md`. Phase 2 implementation is sufficient; further tuning is deferred to the 107 platform. First fix the truth branch's ignored CLI settings and review logistic regression, then establish a baseline. Prioritize the handout deliverables and a manageable validation comparison. Keep new scripts under `scr/p03_*.py` and documents under `docs/p03/`. Inspect current files before editing and preserve Phase 2 behavior.

This guide was checked against the local handout, current scripts, CSV class counts, and feature-file shapes. Task 3 model training was not executed while preparing it.
