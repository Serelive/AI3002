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
        for iter in range(self.max_iter):
            gradient = self._gradient(weights, bias, features, targets)
            weights = weights - self.lr * gradient[0]
            bias = bias - self.lr * gradient[1]
        self.weights, self.bias = weights, bias

    def predict(self, features: np.ndarray) -> np.ndarray:
        # 提示：使用矩阵乘法和偏置，返回形状为 (N,) 的预测值。
        return np.dot(features, self.weights) + self.bias

    def _gradient(
        self,
        weights: np.ndarray,
        bias: np.float64,
        features: np.ndarray,
        targets: np.ndarray,
    ) -> tuple:
        gradient_w = 2 / features.shape[0] * features.T @ (features @ weights + bias - targets) + self.l1 * np.sign(weights) + 2 * self.l2 * weights
        gradient_b = 2 / features.shape[0] * np.sum(features @ weights + bias - targets)
        return gradient_w, gradient_b


class LogisticRegressionModel:
    """用逻辑回归从隐藏表征预测句子真假。"""

    def __init__(self, n_features: int):
        # 提示：单个二分类任务只需要一个权重向量和一个标量偏置。
        self.weights = np.zeros(n_features, dtype=np.float64)
        self.bias = np.float64(0.0)

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None:
        # 训练模型；features 为 (N, 2560)，targets 为 (N,) 的 0/1 标签。
        raise NotImplementedError

    def predict(self, features: np.ndarray) -> np.ndarray:
        # 提示：返回形状为 (N,) 的真类概率，不要在此处做 0.5 阈值化。"""
        raise NotImplementedError
