"""Focused checks for experiment output preservation and numerical failures."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

import p02_comparison as comparison
import train23


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.options = comparison.get_parser().parse_args([
            "--output_dir", str(self.root), "--layers", "11", "--l1", "0",
            "--l2", "0", "--lr", "0.1", "0.01", "0.001", "--max_iter", "2",
        ])

    def test_unique_artifacts_best_selection_and_failed_run(self):
        def run(args):
            if args.lr == 0.001:
                raise FloatingPointError("deliberate failure")
            np.savez(args.output_dir / 'world_layer11.npz',
                     weights=np.full((2, 3), args.lr), bias=np.zeros(2))
            return 1. if args.lr == 0.1 else 5.
        with patch.object(train23, 'main', side_effect=run), contextlib.redirect_stdout(io.StringIO()):
            batch = comparison.run_comparison(self.options)
        table = pd.read_csv(batch / 'comparison.csv')
        self.assertEqual(table.status.tolist(), ['ok', 'ok', 'failed'])
        self.assertEqual(table.run_dir.nunique(), 3)
        with np.load(batch / 'selected/world.npz') as f:
            np.testing.assert_array_equal(f['weights'], np.full((2, 3), .1))
        self.assertEqual(json.loads((batch / 'selected/selection.json').read_text())['mse'], 1.)
        self.assertEqual((batch / 'selected/world-layer.txt').read_text(), '11\n')
        self.assertEqual(len(list(batch.glob('*/world_layer11.npz'))), 2)

    def test_interruption_preserves_completed_row_and_selected_model(self):
        def run(args):
            if args.lr != .1:
                raise KeyboardInterrupt
            np.savez(args.output_dir / 'world_layer11.npz', weights=[1.], bias=[0.])
            return 1.
        with patch.object(train23, 'main', side_effect=run), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                comparison.run_comparison(self.options)
        batch = next(self.root.iterdir())
        self.assertEqual(pd.read_csv(batch / 'comparison.csv').status.tolist(), ['ok', 'interrupted'])
        self.assertTrue((batch / 'selected/world.npz').exists())

    def test_all_failed_has_no_selected_model(self):
        with patch.object(train23, 'main', side_effect=FloatingPointError('overflow')), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'No finite successful runs'):
                comparison.run_comparison(self.options)
        self.assertFalse((next(self.root.iterdir()) / 'selected').exists())

    def test_real_world_export_and_no_overwrite_or_nan_export(self):
        X = np.array([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
        Y = np.column_stack((2 * X[:, 0] + 3, -4 * X[:, 1] + 5))
        args = train23.get_parser().parse_args([
            'world', '11', '--output_dir', str(self.root / 'good'),
            '--lr', '.1', '--l1', '0', '--l2', '0', '--max_iter', '200',
        ])
        with patch.object(train23, 'load_split', return_value=(X, Y)), contextlib.redirect_stdout(io.StringIO()):
            self.assertLess(train23.main(args), 1e-16)
            p = args.output_dir / 'world_layer11.npz'
            original = p.read_bytes()
            with np.load(p) as f:
                np.testing.assert_allclose(X @ f['weights'].T + f['bias'], Y, atol=1e-8)
            with self.assertRaises(FileExistsError):
                train23.main(args)
            self.assertEqual(p.read_bytes(), original)
            args.output_dir = self.root / 'bad'
            args.lr = 1e200
            with self.assertRaises(FloatingPointError):
                train23.main(args)
            self.assertFalse((args.output_dir / 'world_layer11.npz').exists())


if __name__ == '__main__':
    unittest.main()
