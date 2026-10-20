"""Regression checks for stopping boundaries and truth parameter export."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

import train23
from model import LinearRegressionModel, LogisticRegressionModel


class IterationTests(unittest.TestCase):
    def test_final_update_is_checked(self):
        x = np.array([[1.], [2.], [3.], [4.]])
        for cls, y in ((LinearRegressionModel, 2 * x[:, 0] + 1),
                       (LogisticRegressionModel, np.array([0., 0., 1., 1.]))):
            for count in (1, 19, 20, 21):
                with self.subTest(model=cls.__name__, count=count):
                    model = cls(1, lr=.01, max_iter=count)
                    w, b = np.zeros(1), 0.
                    for _ in range(count):
                        dw, db = model._gradient(w, b, x, y)
                        w, b = w - model.lr * dw, b - model.lr * db
                    model.fit(x, y)
                    np.testing.assert_allclose(model.weights, w)
                    np.testing.assert_allclose(model.bias, b)
                    self.assertEqual(model.n_iter_, count)
                    self.assertEqual(model.best_iter_, count)

    def test_small_improvements_are_saved_without_resetting_patience(self):
        for cls in (LinearRegressionModel, LogisticRegressionModel):
            model = cls(1, max_iter=200)
            # Six checkpoints: initial state, then five sub-tolerance decreases.
            with patch.object(model, '_loss', side_effect=1 - np.arange(6) * 1e-8):
                model.fit(np.array([[1.]]), np.array([1.]))
            self.assertEqual(model.n_iter_, 100)
            self.assertEqual(model.best_iter_, 100)
            self.assertEqual(model.stop_reason_, 'patience exhausted')
            self.assertNotEqual(model.weights[0], 0.)

    def test_nonfinite_initial_loss_is_rejected(self):
        for cls in (LinearRegressionModel, LogisticRegressionModel):
            model = cls(1)
            with patch.object(model, '_loss', return_value=float('nan')):
                with self.assertRaises(FloatingPointError):
                    model.fit(np.ones((1, 1)), np.ones(1))

    def test_truth_export_on_real_layer11(self):
        predictions = []
        original_predict = LogisticRegressionModel.predict

        def capture(model, features):
            result = original_predict(model, features)
            predictions.append(result)
            return result

        with tempfile.TemporaryDirectory() as directory:
            args = train23.get_parser().parse_args([
                'truth', '11', '--max_iter', '21', '--output_dir', directory])
            with patch.object(LogisticRegressionModel, 'predict', capture):
                accuracy = train23.main(args)
            x, y = train23.load_split('truth', 'valid', 11)
            with np.load(Path(directory) / 'truth_layer11.npz') as saved:
                self.assertEqual(saved['weights'].shape, (2560,))
                self.assertEqual(saved['bias'].shape, ())
                self.assertEqual(saved['weights'].dtype, np.dtype('float64'))
                self.assertEqual(saved['bias'].dtype, np.dtype('float64'))
                p = np.exp(-np.logaddexp(0., -(x @ saved['weights'] + saved['bias'])))
            np.testing.assert_allclose(p, predictions[0], atol=1e-12)
            self.assertEqual(accuracy, np.mean((p >= .5) == y))

    def test_default_directory(self):
        for task in ('truth', 'world'):
            args = train23.get_parser().parse_args([task, '11'])
            # Stop before loading inputs or writing artifacts.
            with patch.object(train23, 'load_split', side_effect=RuntimeError('stop')), \
                 patch.object(Path, 'exists', return_value=False):
                with self.assertRaisesRegex(RuntimeError, 'stop'):
                    train23.main(args)
            expected = Path(train23.__file__).resolve().parent.parent / 'output' / {'world': 'p02', 'truth': 'p03'}[task]
            self.assertEqual(args.output_dir, expected)


if __name__ == '__main__':
    unittest.main()
