# Task 3 iteration review

I found **two correctness bugs, one output-path issue, and the remaining performance issue**. The loss formulas and gradients are consistent: finite-difference checks passed for both models.

1. **Early stopping discards updates when training ends between checks.**
   In [model.py](../../scr/model.py), lines 42 and 136 at the time of review, you evaluate and save parameters only every 20 updates, then return the saved parameters.

   I reproduced these results for both models:

   - `max_iter=1` or `19`: returns the initial zero parameters.
   - `max_iter=21`: returns the parameters from update 20, discarding update 21.

   Evaluate the final iteration too:

   ```python
   if (i + 1) % check_every == 0 or i + 1 == self.max_iter:
   ```

   Also distinguish **saving the lowest-loss parameters** from **resetting patience after a significant improvement**. Currently, a smaller loss is saved only when it beats the tolerance threshold, so `best_weights` does not necessarily contain the best evaluated parameters. Maintain a separate reference loss for the patience criterion if you want both behaviors.

2. **The truth model still exports incorrect parameters.**
   In [train23.py](../../scr/train23.py), line 147 at the time of review, training and prediction use raw features, but export applies the inverse standardization transformation.

   For your current raw-feature approach, replace the export assignment with:

   ```python
   weights_original = model.weights
   bias_original = model.bias
   ```

   Alternatively, use standardized features for both training and prediction and retain the conversion. In a small reproduction, the current conversion changed predicted probabilities by as much as **0.413**.

3. **The default output directory is one level too deep.**
   [train23.py](../../scr/train23.py), line 80 at the time of review, resolves to `lab1/main/output/truth`, rather than the assignment’s `lab1/output/truth`.

   Use:

   ```python
   args.output_dir = Path(__file__).parent.parent / "output" / args.task
   ```

   Choosing the directory based on `args.task` is correct. Git reported an untracked `../../scr` directory at the time of review.

4. **Both gradients still create the large temporary matrix discussed earlier.**
   See [model.py](../../scr/model.py), lines 92 and 173 at the time of review. Compute the matrix–vector product before scaling:

   ```python
   # Linear regression
   gradient_w = (
       2 * (features.T @ residual) / features.shape[0]
       + self.l1 * np.sign(weights)
       + 2 * self.l2 * weights
   )

   # Logistic regression
   gradient_w = (
       (features.T @ residual) / features.shape[0]
       + self.l1 * np.sign(weights)
       + 2 * self.l2 * weights
   )
   ```

Your patience logic otherwise has a clear interpretation: **five consecutive checks without sufficient improvement**, with checks every 20 updates, means **100 updates without sufficient improvement**. The threshold is absolute when `best_loss` has magnitude below 1 and relative above 1.

Because you monitor **regularized training loss**, this is a convergence stopping rule. It does not detect validation performance deteriorating through overfitting. That is a reasonable initial approach, but it may still run all 10,000 updates if training loss continues improving. Recording `n_iter_` and printing the stopping reason would make runtime easier to understand.

I ran small numerical and boundary checks; I did not run full training or change any code files.
