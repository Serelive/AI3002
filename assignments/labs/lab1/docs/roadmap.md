# Lab 1 roadmap

This roadmap currently covers **p01 / Task 1**: implementing and checking linear and logistic regression, then preparing evidence for report questions 1–3. Tasks 2–3 will be planned separately. Markers follow [the working agreement](agreement.md).

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
