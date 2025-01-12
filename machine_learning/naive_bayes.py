import numpy as np


class NaiveBayesClassifier:
    def __init__(self):
        self.class_probs = {}
        self.feature_probs = {}

    def fit(self, X, y):
        # Calculate prior probabilities (P(class))
        class_counts = y.value_counts()
        total_samples = len(y)
        self.class_probs = class_counts / total_samples


        print("Class Probabilities (Prior):")
        print(self.class_probs)

        # Calculate probabilities (P(feature|class))
        self.feature_probs = {}
        for class_value in self.class_probs.index:
            class_data = X[y == class_value]
            feature_probs_for_class = {}
            for column in X.columns:
                feature_counts = class_data[column].value_counts()
                total_features_in_class = len(class_data)
                feature_probs_for_class[column] = feature_counts / total_features_in_class
            self.feature_probs[class_value] = feature_probs_for_class


        print("Feature Probabilities (Likelihood):")
        for class_value, probs in self.feature_probs.items():
            print(f"Class: {class_value}")
            print(probs)

    def predict(self, X):
        predictions = []
        for _, row in X.iterrows():
            class_probabilities = {}
            for class_value in self.class_probs.index:
                # Start with the prior probability for the class
                class_prob = np.log(self.class_probs[class_value])


                for column in X.columns:
                    feature_value = row[column]
                    feature_prob = self.feature_probs[class_value][column].get(feature_value, 1e-10)  # Small smoothing
                    class_prob += np.log(feature_prob)

                class_probabilities[class_value] = class_prob


            print(f"Row: {row.to_dict()}")
            print(f"Class Probabilities: {class_probabilities}")


            if class_probabilities:
                predicted_class = max(class_probabilities, key=class_probabilities.get)
            else:
                predicted_class = None
            predictions.append(predicted_class)

        return predictions
