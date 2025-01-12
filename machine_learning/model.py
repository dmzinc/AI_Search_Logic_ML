from abc import ABC
import numpy as np

class Model(ABC):
    def fit(self, X: np.array, y: np.array):
        pass
    def predict(self, X: np.array) -> list:
        pass