import numpy as np

class LinearRegressionModel:
    """用单个线性回归模型预测一个连续目标。"""

    def __init__(
        self,
        n_features: int,
        l1: float= 0.0,
        l2: float= 0.0,
        lr: float= 0.01,
        max_iter: int= 10000,
    ) -> None:
        # 一个连续目标只需要一个权重向量和一个标量偏置。
        self.n_features = n_features
        self.weights = np.zeros(n_features, dtype=np.float64)
        self.bias = np.float64(0.0)
        self.l1 = l1
        self.l2 = l2
        self.lr = lr
        self.max_iter = max_iter

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None:
        # 训练模型；features 为 (N, D)，targets 为 (N,)。
        weights = np.zeros(self.n_features, dtype=np.float64)
        bias = np.float64(0.0)

        best_loss = self._loss(weights, bias, features, targets)
        best_weights = weights.copy()
        best_bias = bias

        patience = 5
        counter = 0
        tol = 1e-6
        check_every = 20

        for i in range(self.max_iter):
            grad_w, grad_b = self._gradient(weights, bias, features, targets)
            weights = weights - self.lr * grad_w
            bias = bias - self.lr * grad_b

            if (i+1) % check_every == 0:
                loss = self._loss(weights, bias, features, targets)

                if not np.isfinite(loss):
                    raise FloatingPointError("Loss is not finite")

                threshold = tol * max(1.0, abs(best_loss))

                if loss < best_loss - threshold:
                    best_loss = loss
                    best_weights = weights.copy()
                    best_bias = bias.copy()
                    counter = 0
                else:
                    counter += 1

                if counter >= patience:
                    break

        self.weights, self.bias = best_weights, best_bias

    def predict(self, features: np.ndarray) -> np.ndarray:
        # 提示：使用矩阵乘法和偏置，返回形状为 (N,) 的预测值。
        return np.dot(features, self.weights) + self.bias

    def _loss(
        self,
        weights: np.ndarray,
        bias: np.ndarray,
        features: np.ndarray,
        targets: np.ndarray,
    ) -> float:
        residual = features @ weights + bias - targets
        mce = np.square(residual)
        loss = np.mean(
            mce
            + self.l1 * np.sum(np.abs(weights))
            + self.l2 * np.sum(np.square(weights))
        )
        return loss


    def _gradient(
        self,
        weights: np.ndarray,
        bias: np.float64,
        features: np.ndarray,
        targets: np.ndarray,
    ) -> tuple:
        residual = features @ weights + bias - targets
        gradient_w = 2 / features.shape[0] * features.T @ residual + self.l1 * np.sign(weights) + 2 * self.l2 * weights
        gradient_b = 2 * np.mean(residual)
        return gradient_w, gradient_b


class LogisticRegressionModel:
    """用逻辑回归从隐藏表征预测句子真假。"""

    def __init__(
        self,
        n_features: int,
        l1: float = 0.0,
        l2: float = 0.0,
        lr: float = 0.01,
        max_iter: int = 10000,
    ) -> None:
        # 提示：单个二分类任务只需要一个权重向量和一个标量偏置。
        self.n_features = n_features
        self.weights = np.zeros(n_features, dtype=np.float64)
        self.bias = np.float64(0.0)
        self.l1 = l1
        self.l2 = l2
        self.lr = lr
        self.max_iter = max_iter

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None:
        # 训练模型；features 为 (N, 2560)，targets 为 (N,) 的 0/1 标签。
        weights = np.zeros(self.n_features, dtype=np.float64)
        bias = np.float64(0.0)

        best_loss = self._loss(weights, bias, features, targets)
        best_weights = weights.copy()
        best_bias = bias

        patience = 5
        counter = 0
        tol = 1e-6
        check_every = 20

        for i in range(self.max_iter):
            grad_w, grad_b = self._gradient(weights, bias, features, targets)
            weights = weights - self.lr * grad_w
            bias = bias - self.lr * grad_b

            if (i+1) % check_every == 0:
                loss = self._loss(weights, bias, features, targets)

                if not np.isfinite(loss):
                    raise FloatingPointError("Loss is not finite")

                threshold = tol * max(1.0, abs(best_loss))

                if loss < best_loss - threshold:
                    best_loss = loss
                    best_weights = weights.copy()
                    best_bias = bias.copy()
                    counter = 0
                else:
                    counter += 1

                if counter >= patience:
                    break

        self.weights, self.bias = best_weights, best_bias

    def predict(self, features: np.ndarray) -> np.ndarray:
        # 提示：返回形状为 (N,) 的真类概率，不要在此处做 0.5 阈值化。"""
        scores = features @ self.weights + self.bias
        probabilities = np.exp(-np.logaddexp(0.0, -scores))
        return probabilities

    def _gradient(
        self,
        weights: np.ndarray,
        bias: np.float64,
        features: np.ndarray,
        targets: np.ndarray,
    ) -> tuple:
        scores = features @ weights + bias
        probabilities = np.exp(-np.logaddexp(0.0, -scores))
        residual = probabilities - targets
        gradient_w = 1 / features.shape[0] * features.T @ residual + self.l1 * np.sign(weights) + 2 * self.l2 * weights
        gradient_b = np.mean(residual)
        return gradient_w, gradient_b

    def _loss(
        self,
        weights: np.ndarray,
        bias: float,
        features: np.ndarray,
        targets: np.ndarray,
    ) -> float:
        scores = features @ weights + bias
        bce = np.mean(
            np.logaddexp(0.0, scores) - targets * scores
        )
        return float(
            bce
            + self.l1 * np.sum(np.abs(weights))
            + self.l2 * np.sum(weights ** 2)
        )
