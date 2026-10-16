"""Compare world probes, saving each configuration and the best finite model."""

import argparse
from datetime import datetime
from itertools import product
import json
from pathlib import Path
import shutil
from time import perf_counter

import numpy as np
import pandas as pd

import train23

LAYERS = (11, 23, 35)
L1 = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
L2 = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
LR = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
MAX_ITER = 10000


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output_dir", type=Path,
                        default=Path(__file__).resolve().parent.parent / "output" / "p02" / "comparison")
    parser.add_argument("--layers", type=int, nargs="+", choices=LAYERS, default=LAYERS)
    parser.add_argument("--l1", type=float, nargs="+", default=L1)
    parser.add_argument("--l2", type=float, nargs="+", default=L2)
    parser.add_argument("--lr", type=float, nargs="+", default=LR)
    parser.add_argument("--max_iter", type=int, default=MAX_ITER)
    return parser


def run_comparison(options):
    for name in ("l1", "l2", "lr"):
        values = np.asarray(getattr(options, name))
        if not np.isfinite(values).all() or (values < 0).any() or (name == "lr" and (values == 0).any()):
            raise ValueError("Require finite l1/l2 >= 0 and lr > 0")
    if options.max_iter <= 0:
        raise ValueError("max_iter must be positive")

    # A new batch keeps reruns and separate PCs' results independent.
    batch = options.output_dir / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    batch.mkdir(parents=True, exist_ok=False)
    print(f"Results: {batch.resolve()}", flush=True)
    records = []
    best = None
    parser = train23.get_parser()
    grid = product(options.layers, options.l1, options.l2, options.lr)
    for index, (layer, l1, l2, lr) in enumerate(grid, start=1):
        run_name = f"{index:04d}_layer{layer}_l1-{l1:g}_l2-{l2:g}_lr-{lr:g}"
        run_dir = batch / run_name
        run_dir.mkdir()
        args = parser.parse_args(["world", str(layer)])
        args.l1, args.l2, args.lr = l1, l2, lr
        args.max_iter, args.output_dir = options.max_iter, run_dir
        record = dict(layer=layer, l1=l1, l2=l2, lr=lr,
                      max_iter=options.max_iter, run_dir=run_name,
                      status="running", mse=None, error="")
        # Retain settings even if this run is interrupted.
        (run_dir / "config.json").write_text(json.dumps(record, indent=2) + "\n")
        started = perf_counter()
        try:
            print(f"Running {run_name}", flush=True)
            mse = float(train23.main(args))
            if not np.isfinite(mse):
                raise FloatingPointError("Non-finite validation MSE")
            record.update(status="ok", mse=mse)
        except FloatingPointError as exc:
            record.update(status="failed", error=str(exc))
            print(f"Failed {run_name}: {exc}", flush=True)
        except KeyboardInterrupt:
            record.update(status="interrupted", error="KeyboardInterrupt")
            raise
        except Exception as exc:
            record.update(status="error", error=f"{type(exc).__name__}: {exc}")
            raise
        finally:
            record["seconds"] = perf_counter() - started
            records.append(record)
            (run_dir / "result.json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
            temporary_csv = batch / "comparison.csv.tmp"
            pd.DataFrame(records).to_csv(temporary_csv, index=False)
            temporary_csv.replace(batch / "comparison.csv")

        if record["status"] == "ok" and (best is None or record["mse"] < best["mse"]):
            selected = batch / "selected"
            selected.mkdir(exist_ok=True)
            shutil.copy2(run_dir / f"world_layer{layer}.npz", selected / "world.npz")
            (selected / "world-layer.txt").write_text(f"{layer}\n")
            best = record.copy()
            (selected / "selection.json").write_text(json.dumps(best, indent=2) + "\n")

    if best is None:
        raise RuntimeError(f"No finite successful runs; inspect {batch / 'comparison.csv'}")
    print(f"Best: {best}\nSelected model: {batch / 'selected' / 'world.npz'}", flush=True)
    return batch


def main():
    run_comparison(get_parser().parse_args())


if __name__ == "__main__":
    main()
