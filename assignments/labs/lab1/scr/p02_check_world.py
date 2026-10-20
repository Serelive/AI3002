"""Check the six supplied world input pairs without changing their row order."""

from pathlib import Path

import numpy as np
import pandas as pd

from train23 import load_split

SPLITS = ("train", "valid")
LAYERS = (11, 23, 35)


def main() -> None:
    data_dir = Path(__file__).resolve().parent / "datasets" / "world"
    for split in SPLITS:
        expected_rows = 500 if split == "train" else 130
        labels = pd.read_csv(data_dir / f"{split}.csv")
        expected_targets = labels[["latitude", "longitude"]].to_numpy(
            dtype=np.float64
        )
        first_layer_targets = None

        for layer in LAYERS:
            X, Y = load_split("world", split, layer)
            context = f"{split}, layer {layer}"
            assert X.shape == (expected_rows, 2560), f"{context}: wrong X shape"
            assert Y.shape == (expected_rows, 2), f"{context}: wrong Y shape"
            assert X.dtype == np.float64, f"{context}: X must be float64"
            assert Y.dtype == np.float64, f"{context}: Y must be float64"
            assert np.isfinite(X).all(), f"{context}: X contains NaN or infinity"
            assert np.isfinite(Y).all(), f"{context}: Y contains NaN or infinity"
            assert (np.abs(Y[:, 0]) <= 90).all(), f"{context}: latitude out of bounds"
            assert (np.abs(Y[:, 1]) <= 180).all(), f"{context}: longitude out of bounds"
            np.testing.assert_array_equal(
                Y, expected_targets,
                err_msg=f"{context}: targets differ from CSV latitude/longitude order",
            )
            if first_layer_targets is None:
                first_layer_targets = Y.copy()
            else:
                np.testing.assert_array_equal(
                    Y, first_layer_targets,
                    err_msg=f"{context}: targets differ across layers",
                )
            print(f"Task: world, split: {split}, layer: {layer} passed.")

    print("PASS: 6 input pairs")


if __name__ == "__main__":
    main()
