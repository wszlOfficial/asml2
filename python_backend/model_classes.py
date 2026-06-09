import numpy as np

class Node():
    def __init__(self, feature=None, threshold=None, *, value=None, left=None, right=None):
        self.feature = feature
        self.threshold = threshold
        self.value = value
        self.left = left
        self.right = right



class NumDecisionTree():    
    def __init__(self):
        self.root = None


    def grow_tree(self, x, y, *, max_depth=3, max_features=None):
        self.x_train = x
        self.y_train = y
        self.max_features = max_features if max_features else x.shape[1]
        
        self.root = self._grow_tree_helper(max_depth, np.arange(len(self.y_train)))


    def _grow_tree_helper(self, depth, indices):
        y_node = self.y_train.values[indices]

        # Base case: check if node is a leaf node
        if len(np.unique(y_node)) == 1:
            return Node(value=y_node[0])
        
        # Base case: max depth reached
        if depth == 0:
            #most_common = np.bincount(y_node).argmax()
            return Node(value=np.mean(y_node))
        
        # Find the best split for this node
        feature, threshold = self.find_best_split(indices)

        if feature == None:  # No valid split is found
            #most_common = np.bincount(y_node).argmax()
            return Node(value=np.mean(y_node))
        
        # Which of our current indices go left/right?
        feat_values = self.x_train[feature].values[indices]
        left_mask = feat_values <= threshold
        
        # Sub-divide the indices
        left_indices = indices[left_mask]
        right_indices = indices[~left_mask]

        left_child = self._grow_tree_helper(depth - 1, left_indices)
        right_child = self._grow_tree_helper(depth - 1, right_indices)

        return Node(feature, threshold, left=left_child, right=right_child)


    def find_best_split(self, indices):
        n_total = len(indices)
        #best_gini = 1.0
        best_variance = 999999999999.0
        best_threshold, best_feature = None, None
        
        x_node = self.x_train.values[indices]
        y_node = self.y_train.values[indices]

        # Loop through features by index
        for feature in range(x_node.shape[1]):
            # Use a view of the column
            column_values = x_node[:, feature]
            thresholds = np.unique(column_values)
            
            for threshold in thresholds:
                left_mask = column_values <= threshold
                
                y_left = y_node[left_mask]
                y_right = y_node[~left_mask]

                # Skip invalid splits
                if y_left.size == 0 or y_right.size == 0:
                    continue
                
                # Calculate means and variances
                mean_left = np.mean(y_left)
                var_left = np.mean((y_left - mean_left) **2)
                mean_right = np.mean(y_right)
                var_right = np.mean((y_right - mean_right) **2)
                
                # Weighted average
                w_left = y_left.size / n_total
                weighted_variance = (w_left * var_left) + ((1.0 - w_left) * var_right)

                # Check if this is the best split
                if weighted_variance < best_variance:
                    best_variance = weighted_variance
                    best_threshold = threshold
                    best_feature = self.x_train.columns[feature]
    
        return best_feature, best_threshold

    
    def predict(self, x):
        if self.root is None:  # Tree has not been grown yet
            raise AttributeError("Can't predict values for this tree as it hasn't been grown yet. Call grow_tree() before predicting.")
        return np.array([self._traverse(row) for _, row in x.iterrows()])


    def _traverse(self, row, node=None):  # Recursive function for traversing through a tree
        if node is None:
            node = self.root
        
        if node.value is not None:  # Node is a leaf
            return node.value
        
        if row[node.feature] <= node.threshold:
            return self._traverse(row, node.left)
        return self._traverse(row, node.right) 
    


class NumRandomForest():
    def __init__(self, n_trees=10, max_depth=3, max_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.max_features = max_features
        self.trees = []

    def fit(self, x, y):
        self.trees = []
        for _ in range(self.n_trees):
            sample_idx = np.random.choice(len(y), size=len(y), replace=True)
            x_sample = x.iloc[sample_idx].reset_index(drop=True)
            y_sample = y.iloc[sample_idx].reset_index(drop=True)

            tree = NumDecisionTree()
            tree.grow_tree(x_sample, y_sample,
                           max_depth=self.max_depth,
                           max_features=self.max_features)
            self.trees.append(tree)

    def predict(self, x):
        # Stack predictions from all trees: shape will be (n_trees, n_samples)
        all_preds = np.vstack([tree.predict(x) for tree in self.trees])
        
        # Calculate the average prediction across all trees (axis 0)
        return np.mean(all_preds, axis=0)    



class CatDecisionTree():    
    def __init__(self):
        self.root = None

    def grow_tree(self, x, y, *, max_depth=3, max_features=None):
        self.x_train = x
        self.y_train = y
        self.max_features = max_features if max_features else x.shape[1]
        
        self.root = self._grow_tree_helper(max_depth, np.arange(len(self.y_train)))

    def _grow_tree_helper(self, depth, indices):
        y_node = self.y_train.values[indices]

        # Base case: check if node is a leaf node
        if len(np.unique(y_node)) == 1:
            return Node(value=y_node[0])
        
        # Base case: max depth reached
        if depth == 0:
            most_common = np.bincount(y_node).argmax()
            return Node(value=most_common)
        
        # Find the best split for this node
        feature, threshold = self.find_best_split(indices)

        if feature == None:  # No valid split is found
            most_common = np.bincount(y_node).argmax()
            return Node(value=most_common)
        
        # Which of our current indices go left/right?
        feat_values = self.x_train[feature].values[indices]
        left_mask = feat_values <= threshold
        
        # Sub-divide the indices
        left_indices = indices[left_mask]
        right_indices = indices[~left_mask]

        left_child = self._grow_tree_helper(depth - 1, left_indices)
        right_child = self._grow_tree_helper(depth - 1, right_indices)

        return Node(feature, threshold, left=left_child, right=right_child)

    def find_best_split(self, indices):
        n_total = len(indices)
        best_gini = 1.0
        best_threshold, best_feature = None, None
        
        x_node = self.x_train.values[indices]
        y_node = self.y_train.values[indices]

        usable_columns = np.random.choice(
            x_node.shape[1],
            size=min(self.max_features, x_node.shape[1]),
            replace=False
        )

        # Loop through features by index
        for feature in usable_columns:
            # Use a view of the column
            column_values = x_node[:, feature]
            thresholds = np.unique(column_values)
            
            for threshold in thresholds:
                left_mask = column_values <= threshold
                
                y_left = y_node[left_mask]
                y_right = y_node[~left_mask]

                # Skip invalid splits
                if y_left.size == 0 or y_right.size == 0:
                    continue

                # Calculate Gini
                g_left = self.gini(y_left)
                g_right = self.gini(y_right)
                
                # Weighted average
                w_left = y_left.size / n_total
                weighted_gini = (w_left * g_left) + ((1.0 - w_left) * g_right)

                if weighted_gini < best_gini:
                    best_gini = weighted_gini
                    best_threshold = threshold
                    best_feature = self.x_train.columns[feature]
    
        return best_feature, best_threshold

    def gini(self, subset):
        # G = 1-sum(p_i^2)
        _, counts = np.unique(subset, return_counts=True)  # How many occurances per label
        probabilities = counts / len(subset)
        return 1.0 - np.sum(probabilities**2)
    
    def predict(self, x):
        if self.root is None:  # Tree has not been grown yet
            raise AttributeError("Can't predict values for this tree as it hasn't been grown yet. Call grow_tree() before predicting.")
        return np.array([self._traverse(row) for _, row in x.iterrows()])

    def _traverse(self, row, node=None):  # Recursive function for traversing through a tree
        if node is None:
            node = self.root
        
        if node.value is not None:  # Node is a leaf
            return node.value
        
        if row[node.feature] <= node.threshold:
            return self._traverse(row, node.left)
        return self._traverse(row, node.right)
    


class CatRandomForest():
    def __init__(self, n_trees=10, max_depth=3, max_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.max_features = max_features
        self.trees = []

    def fit(self, x, y):
        self.trees = []
        for _ in range(self.n_trees):
            sample_idx = np.random.choice(len(y), size=len(y), replace=True)
            x_sample = x.iloc[sample_idx].reset_index(drop=True)
            y_sample = y.iloc[sample_idx].reset_index(drop=True)

            tree = CatDecisionTree()
            tree.grow_tree(x_sample, y_sample,
                           max_depth=self.max_depth,
                           max_features=self.max_features)
            self.trees.append(tree)

    def predict(self, x):
        all_preds = np.vstack([tree.predict(x) for tree in self.trees])
        # majority vote across trees
        return np.apply_along_axis(lambda col: np.bincount(col).argmax(), axis=0, arr=all_preds)