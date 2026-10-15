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

Source: `docs/instruction.pdf` §2.2, with export details in Appendix C.1. Detailed main-body guides: [English](p02/p02_guide_main-eng.md) and [中文](p02/p02_guide_main-zh.md). These are plans, not completed experiment results.

### Main implementation

Use the [actionable main checklist](p02/p02_checklist_main.md) for exact edits, hand-in artifacts, commands, and pass/fail criteria. It follows the October 15 CLI; the older guides' CLI examples predate that interface. Submit one checklist step at a time. The suffixes below split the existing increments without renumbering later work.

| Increment | Concrete deliverable | Checklist step |
| --- | --- | --- |
| `p02-i00` | Save the regression-test results and current CLI help in `start-check.txt`. | 1 |
| `p02-i01` | Write `check_world.py`; assert the six input pairs' shapes, types, finite values, and target order. | 2 |
| `p02-i02` | Write a two-output toy check with known weights and biases; assert prediction and parameter equality. | 3 |
| `p02-i03a` | Reject invalid CLI settings and existing output files; capture rejection evidence. | 4 |
| `p02-i03b` | Record training-objective history and actual iterations; fail on non-finite inputs or updates. | 5 |
| `p02-i03c` | Compute a conservative rate and save finite, decreasing-loss layer-11 baseline runs. | 6 |
| `p02-i04` | Export configuration, train/validation metrics, training-mean baseline, histories, and ordered predictions per run. | 7 |
| `p02-i05a` | Execute the recorded 15-configuration layer/L2 plan and aggregate results, including failures. | 8 |
| `p02-i05b` | Repeat the best candidates with larger iteration budgets and record a selection using the predefined rule. | 9 |
| `p02-i06` | Write a fresh-process export checker; assert schema, raw-feature predictions, and metric equality. | 10 |
| `p02-i07` | Reproduce the selected run, save the candidate and layer file, and record exact commands in the README. | 11 |

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
