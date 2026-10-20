# Lab 1 roadmap

This roadmap covers **p01 / Task 1**, **p02 / Task 2**, and **p03 / Task 3**. Phase 2 implementation is sufficient for moving on; further refinement is deferred to the 107 platform. Markers follow [the working agreement](agreement.md).

## p01 — Models and supporting experiments

| Increment | Goal |
| --- | --- |
| `p01-i00` | Connect the equations in `instruction.pdf` §2.1 to `scr/model.py`: array shapes, predictions, losses, gradients, and parameter updates. |
| `p01-i01` | Implement `LinearRegressionModel.fit()` using NumPy gradient descent, L1/L2 regularization, and a stopping rule; leave the bias unregularized. |
| `p01-i02` | Implement `LinearRegressionModel.predict()` with one prediction per input row. |
| `p01-i03` | Check and debug linear regression on small known examples, including gradient updates and regularization behavior. |
| `p01-i04` | Implement `LogisticRegressionModel.fit()` with stable numerical calculations, L1/L2 regularization, and a stopping rule; leave the bias unregularized. |
| `p01-i05` | Implement `LogisticRegressionModel.predict()` to return probabilities, not thresholded labels. |
| `p01-i06` | Check and debug logistic regression, including probability bounds, extreme scores, and regularization; run both models through `scr/train1.py`. |
| `p01-i07` | Question 1: reproduce L1/L2 coefficient paths and explain the data source (slides pp. 42 and 48). |
| `p01-i08` | Question 2: construct an example showing why zeroing small L2 coefficients can be a poor feature-selection method compared with L1 (slides p. 44). |
| `p01-i09` | Question 3: compare fitting results with scikit-learn under comparable settings. Finalize the answer after Tasks 2–3 if useful. |
| `p01-i10` | Review Task 1 code and report evidence, record reproduction commands, and prepare the models for Tasks 2–3. |

Paths above are relative to `lab1`, except `instruction.pdf`, which is in `docs/`. Consult the referenced slides before designing the coefficient-path experiments.

**Completion check:** both models run correctly; checks and experiments are reproducible; questions 1–2 have supporting evidence; question 3 is answered or explicitly deferred. This completes Task 1 preparation, not the full lab submission.

## p02 — Predict geographic coordinates

Status: implemented sufficiently according to the learner. Promising layers are 11/35, with L1/L2 around 0.3–1.0 and learning rate around 0.0001. Further tuning continues on the 107 platform; retain existing artifacts and report evidence.

Source: `docs/instruction.pdf` §2.2, with export details in Appendix C.1. Detailed main-body guides: [English](p02/p02_guide_main-eng.md) and [中文](p02/p02_guide_main-zh.md). These are plans, not completed experiment results.

### Main implementation — minimal path

Follow the [minimal main checklist](p02/p02_checklist_main.md). It replaces the eleven-step workflow; the detailed guides are optional references. The handout gives Task 3 more model-performance weight, so prioritize these outcomes and limit Task 2 tuning.

| Priority / increment | Outcome |
| --- | --- |
| Already complete: `p02-i00`, `p02-i01` | Regression/CLI and input checks passed; reuse the results. |
| Highest: `p02-i03` | Train one working two-output coordinate predictor; obtain finite validation predictions and save its weights. Library-trained final weights are permitted by §2.2. |
| Next: `p02-i05` | Make a small layer/regularization comparison using validation MSE; record the selected settings. No fixed search grid is required. |
| Essential finish: `p02-i06` | Save the specified float64 weight/bias arrays and layer; reload once and compare raw-feature predictions. Retain the runnable code and command. |

The old additional implementation gates are retired, not unfinished prerequisites. Add engineering refinements only when they solve a concrete problem. **Main-body completion:** a working selected model, correctly formatted `.npz`, a recorded layer, and a runnable command. Report work and full-lab packaging remain separate.

### Report questions — deferred

| Increment | Later work |
| --- | --- |
| `p02-i08` | Question 4: compare layers, explain the observed differences, and justify the selected layer. |
| `p02-i09` | Question 5: explain the final regularization choice using recorded experiments. |
| `p02-i10` | Question 6: present validation predictions and visualize them on a map, following the handout's map requirements. |
| `p02-i11` | Question 7: assess the strength of evidence for geographic representations versus country recognition. |
| `p02-i12` | Check Task 2 code, selected weights/layer, and answers 4–7 against the prompt; integrate with the full-lab report and packaging. |

Other-layer extraction is optional. Final Task 2 weights may be library-trained, but the lab still requires the handwritten Task 1 training implementation. No hidden-test scores or grading thresholds are assumed.

## p03 — Classify sentence truth

Follow the [p03 guide and handoff](p03/p03_guide_main.md), based on `instruction.pdf` §2.3. Prioritize a working baseline, model selection, and the required export.

| Increment | Outcome |
| --- | --- |
| `p03-i00` | Pass CLI training settings into the truth model and perform a focused logistic-regression check. |
| `p03-i01` | Train a finite baseline and record training/validation accuracy. |
| `p03-i02` | Compare supplied layers and regularization; select by validation accuracy. |
| `p03-i03` | Verify raw-feature inference from float64 weights `(2560,)` and scalar bias `()`; record the layer and reproduction command. |
| `p03-i04` | Answer report questions 8–9 using observed split differences and selection results. |

New files use `scr/p03_*.py` and `docs/p03/`. Retain Phase 2 behavior when editing shared model or training code.
