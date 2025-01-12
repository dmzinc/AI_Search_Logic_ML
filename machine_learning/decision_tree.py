import numpy as np
import matplotlib.pyplot as plt

class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.tree = self._build_tree(X, y)

    def _build_tree(self, X, y, depth=0):
        if len(set(y)) == 1:
            return {'label': y.iloc[0]}

        if self.max_depth is not None and depth >= self.max_depth:
            return {'label': y.mode()[0]}

        if X.empty:
            return {'label': y.mode()[0]}

        best_feature, best_split, best_gini = self._best_split(X, y)

        left_indices = X[best_feature] <= best_split
        right_indices = X[best_feature] > best_split
        left_tree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_tree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return {
            'feature': best_feature,
            'split': best_split,
            'left': left_tree,
            'right': right_tree
        }

    def _best_split(self, X, y):
        best_feature = None
        best_split = None
        best_gini = float('inf')

        for feature in X.columns:
            possible_splits = X[feature].unique()

            for split in possible_splits:
                left_indices = X[feature] <= split
                right_indices = X[feature] > split
                left_y = y[left_indices]
                right_y = y[right_indices]

                gini = self._gini_index(left_y, right_y)

                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_split = split

        return best_feature, best_split, best_gini

    def _gini_index(self, left_y, right_y):
        total_len = len(left_y) + len(right_y)
        left_weight = len(left_y) / total_len
        right_weight = len(right_y) / total_len

        def gini(y):
            _, counts = np.unique(y, return_counts=True)
            probs = counts / len(y)
            return 1 - np.sum(probs ** 2)

        left_gini = gini(left_y)
        right_gini = gini(right_y)

        return left_weight * left_gini + right_weight * right_gini

    def predict(self, X):
        return [self._predict_row(x, self.tree) for _, x in X.iterrows()]

    def _predict_row(self, row, tree):
        if 'label' in tree:
            return tree['label']

        feature = tree['feature']
        split = tree['split']

        if row[feature] <= split:
            return self._predict_row(row, tree['left'])
        else:
            return self._predict_row(row, tree['right'])

    # Textual representation of the tree
    def print_tree(self, tree=None, depth=0):
        if tree is None:
            tree = self.tree


        if 'label' in tree:
            print(f"{'  ' * depth}Predict: {tree['label']}")
            return


        print(f"{'  ' * depth}{tree['feature']} <= {tree['split']}?")
        print(f"{'  ' * (depth + 1)}Left:")
        self.print_tree(tree['left'], depth + 1)
        print(f"{'  ' * (depth + 1)}Right:")
        self.print_tree(tree['right'], depth + 1)

    # Graphical visualization of the tree
    def visualize(self, tree=None, depth=0, x=0.5, y=1, x_offset=0.25, y_offset=0.1, ax=None):
        if tree is None:
            tree = self.tree

        # Initialize the plot if it's the first call
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis("off")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

        # Draw a leaf node
        if 'label' in tree:
            ax.text(x, y, f"Predict: {tree['label']}", fontsize=10, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgreen"))
            return

        # Draw a decision node
        feature = tree['feature']
        split = tree['split']
        ax.text(x, y, f"{feature} <= {split}", fontsize=10, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightblue"))

        # Left subtree
        left_x = x - x_offset
        left_y = y - y_offset
        ax.plot([x, left_x], [y - 0.02, left_y + 0.02], color="black")  # Line to left child
        self.visualize(tree['left'], depth + 1, left_x, left_y, x_offset * 0.5, y_offset, ax)

        # Right subtree
        right_x = x + x_offset
        right_y = y - y_offset
        ax.plot([x, right_x], [y - 0.02, right_y + 0.02], color="black")  # Line to right child
        self.visualize(tree['right'], depth + 1, right_x, right_y, x_offset * 0.5, y_offset, ax)

        # Show the final plot
        if depth == 0:
            plt.show()