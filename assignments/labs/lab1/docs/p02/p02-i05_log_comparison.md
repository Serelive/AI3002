# p02-i05 comparison notes

Standardization is implemented. The initial grid compared three layers and five values each for L1, L2, and learning rate (375 configurations).

The selected result reported by the learner was layer 11, L1 = 0.1, L2 = 0.1, learning rate = 0.0001, and 10,000 updates, with validation MSE **176.64373815281513**. Its record lists 24.55 seconds; the learner also observed roughly seven seconds per run in other experiments. Runtime varies, so the earlier 30-second planning estimate is superseded by measured run records.

Both selected penalties were at the initial grid's upper boundary. The current follow-up defaults compare layers 11, 23, and 35 with L1/L2 values `[0.2, 0.3, 1.0]`, learning rate `0.0001`, and 10,000 updates: **27 configurations**. Keep the initial selected model for comparison, since the follow-up grid does not include 0.1.

The historical terminal transcript is retained locally at `output/p02/p02-i05_log_comparison.txt`. It contains an interrupted early run whose weight files shared a path. New runs save separate configurations and a selected model under `output/p02/comparison/`.
