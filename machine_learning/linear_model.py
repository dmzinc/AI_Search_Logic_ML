import numpy as np
import matplotlib.pyplot as plt
from machine_learning.model import Model

class LinearRegression(Model):

    def fit(self, X: np.array, y: np.array, learning_rate: float = 0.01, epochs: int = 1000) -> Model:
        # Initialize parameters (weights and bias)
        self.theta = np.zeros(X.shape[1])  # Weights
        self.bias = 0  # Bias term

        # To track the loss
        self.losses = []

        # Gradient Descent
        for epoch in range(epochs):
            # Predictions
            predictions = self.predict(X)

            # Calculate error (residuals)
            residuals = predictions - y


            d_theta = (1 / X.shape[0]) * np.dot(X.T, residuals)
            d_bias = (1 / X.shape[0]) * np.sum(residuals)


            self.theta -= learning_rate * d_theta
            self.bias -= learning_rate * d_bias

            # Compute and store the loss
            loss = (1 / (2 * X.shape[0])) * np.sum(residuals ** 2)
            self.losses.append(loss)


            if epoch % 100 == 0:
                print(f"Epoch {epoch}: Loss {loss}")

        return self

    def predict(self, X: np.array) -> np.array:
        return np.dot(X, self.theta) + self.bias

    def plot_loss(self):
        # Plotting the loss over iterations
        plt.plot(range(len(self.losses)), self.losses)
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.title('Loss Reduction over Time')
        plt.show()
