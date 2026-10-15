"""Focused linear-regression checks; run this file directly from the root venv."""

import unittest

import numpy as np

from model import LinearRegressionModel


class LinearRegressionTests(unittest.TestCase):
    def test_two_updates_use_current_parameters(self):
        model = LinearRegressionModel(1, lr=0.1, max_iter=2)
        model.fit(np.array([[1.0]]), np.array([1.0]))
        # First step: (0.2, 0.2); second residual: -0.6.
        np.testing.assert_allclose(model.weights, [0.32])
        np.testing.assert_allclose(model.bias, 0.32)

    def test_gradient_uses_arguments_not_stored_state(self):
        x = np.array([[1., 2.], [-1., 0.], [2., -1.]])
        y = np.array([2., -1., 3.])
        parameters = np.array([0.7, -0.2, 0.3])
        for l1, l2 in [(0., 0.), (0.3, 0.), (0., 0.4), (0.3, 0.4)]:
            with self.subTest(l1=l1, l2=l2):
                model = LinearRegressionModel(2, l1=l1, l2=l2)
                model.weights[:] = 100.
                model.bias = -50.

                def loss(p):
                    return (np.mean((x @ p[:2] + p[2] - y) ** 2)
                            + l1 * np.abs(p[:2]).sum()
                            + l2 * (p[:2] ** 2).sum())

                h = 1e-6
                numerical = [(loss(parameters + h * e) - loss(parameters - h * e))
                             / (2 * h) for e in np.eye(3)]
                dw, db = model._gradient(parameters[:2], parameters[2], x, y)
                np.testing.assert_allclose(np.r_[dw, db], numerical, atol=1e-8)

    def test_toy_fit_and_refit(self):
        x = np.array([[-2, -1], [-1, -1], [-1, 1], [0, -1],
                      [0, 1], [1, -1], [1, 1], [2, 1]], dtype=float)
        y = 2 * x[:, 0] - x[:, 1] + 1
        model = LinearRegressionModel(2)
        for _ in range(2):
            model.fit(x, y)
            np.testing.assert_allclose(model.weights, [2., -1.], atol=1e-8)
            np.testing.assert_allclose(model.bias, 1., atol=1e-8)
            self.assertEqual(model.predict(x).shape, (8,))
            self.assertLess(np.mean((model.predict(x) - y) ** 2), 1e-16)


if __name__ == "__main__":
    unittest.main()
