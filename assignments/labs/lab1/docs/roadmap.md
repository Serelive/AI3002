# Lab 1 roadmap

This roadmap covers **p01 / Task 1** and **p02 / Task 2**. Task 2's main implementation is planned below; its report questions are listed separately for later work. Task 3 will be planned separately. Markers follow [the working agreement](agreement.md).

## p01 — Models and supporting experiments

| Increment | Goal |
| --- | --- |
| `p01-i00` | Connect the equations in `instruction.pdf` §2.1 to `main/model.py`: array shapes, predictions, losses, gradients, and parameter updates. |
| `p01-i01` | Implement `LinearRegressionModel.fit()` using NumPy gradient descent, L1/L2 regularization, and a stopping rule; leave the bias unregularized. |
| `p01-i02` | Implement `LinearRegressionModel.predict()` with one prediction per input row. |
| `p01-i03` | Check and debug linear regression on small known examples, including gradient updates and regularization behavior. |
| `p01-i04` | Implement `LogisticRegressionModel.fit()` with stable numerical calculations, L1/L2 regularization, and a stopping rule; leave the bias unregularized. |
| `p01-i05` | Implement `LogisticRegressionModel.predict()` to return probabilities, not thresholded labels. |
| `p01-i06` | Check and debug logistic regression, including probability bounds, extreme scores, and regularization; run both models through `main/train1.py`. |
| `p01-i07` | Question 1: reproduce L1/L2 coefficient paths and explain the data source (slides pp. 42 and 48). |
| `p01-i08` | Question 2: construct an example showing why zeroing small L2 coefficients can be a poor feature-selection method compared with L1 (slides p. 44). |
| `p01-i09` | Question 3: compare fitting results with scikit-learn under comparable settings. Finalize the answer after Tasks 2–3 if useful. |
| `p01-i10` | Review Task 1 code and report evidence, record reproduction commands, and prepare the models for Tasks 2–3. |

Paths above are relative to `lab1`, except `instruction.pdf`, which is in `docs/`. Consult the referenced slides before designing the coefficient-path experiments.

**Completion check:** both models run correctly; checks and experiments are reproducible; questions 1–2 have supporting evidence; question 3 is answered or explicitly deferred. This completes Task 1 preparation, not the full lab submission.

## p02 — Predict geographic coordinates

Source: `docs/instruction.pdf` §2.2, with export details in Appendix C.1. Detailed main-body guides: [English](p02/p02_guide_main-eng.py) (documentation-only Python file, as requested) and [中文](p02/p02_guide_main-zh.md). These are plans, not completed experiment results.

### Main implementation

| Increment | Goal and completion evidence |
| --- | --- |
| `p02-i00` | Check the Task 1 linear model and trace `train23.py`'s world branch; identify current defaults and missing experiment controls. Logistic-regression review is not a prerequisite for Task 2. |
| `p02-i01` | Validate world inputs and row alignment: 500 training / 130 validation rows, 2,560 features, layers 11/23/35, targets ordered latitude then longitude; compute in float64. |
| `p02-i02` | Confirm the two independent regressions implement the double-output map; verify `(N, 2)` predictions and `X @ W.T + b` equivalence. |
| `p02-i03` | Expose training settings, add finite-value checks and training logs, and establish a stable layer-11 baseline before searching. |
| `p02-i04` | Record training/validation MSE, per-coordinate errors, a training-mean baseline, runtime, configuration, and ordered validation predictions under `output/p02/`. |
| `p02-i05` | Compare supplied layers and a small regularization grid using validation data; check convergence and document the selection rule. Fit preprocessing only on training data if used. |
| `p02-i06` | Export and reload float64 `weights (2, 2560)` and `bias (2,)`, latitude first; fold any preprocessing into raw-feature parameters and check prediction equality. Record the layer separately. |
| `p02-i07` | Reproduce the selected candidate in a fresh process; record its exact command and evidence in the lab README. Select submission files deliberately when packaging begins. |

**Main-body completion check:** a reproducible validation-selected configuration, finite predictions, verified raw-feature inference from the saved `.npz`, and a recorded layer integer. The detailed guides defer questions 4–7; this milestone does not complete the report or full lab.

### Report questions — deferred

| Increment | Later work |
| --- | --- |
| `p02-i08` | Question 4: compare layers, explain the observed differences, and justify the selected layer. |
| `p02-i09` | Question 5: explain the final regularization choice using recorded experiments. |
| `p02-i10` | Question 6: present validation predictions and visualize them on a map, following the handout's map requirements. |
| `p02-i11` | Question 7: assess the strength of evidence for geographic representations versus country recognition. |
| `p02-i12` | Check Task 2 code, selected weights/layer, and answers 4–7 against the prompt; integrate with the full-lab report and packaging. |

Other-layer extraction is optional. Final Task 2 weights may be library-trained, but the lab still requires the handwritten Task 1 training implementation. No hidden-test scores or grading thresholds are assumed.
