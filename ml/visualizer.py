import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from xgboost import plot_importance
from xgboost import plot_tree

class Visualizer:
    def __init__(self):
        pass

    def plot_histogram(self, df: pd.DataFrame):
        """Plot histograms for each numerical column."""
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or not provided.")
        
        numeric_columns = df.select_dtypes(include=['number']).columns
        for column in numeric_columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[column], bins=30, kde=True)
            plt.title(f'Histogram of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.savefig(f'images/histogram_{column}.svg')
            plt.close()

    def plot_confusion_matrix(self, y_true, y_pred, labels):
        """Plot confusion matrix."""
        from sklearn.metrics import confusion_matrix
        import seaborn as sns
        import matplotlib.pyplot as plt

        cm = confusion_matrix(y_true, y_pred, labels=labels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.savefig('images/confusion_matrix.svg')
        plt.close()

    def plot_xgboost_importance(self, model, feature_names):
        """Plot feature importance from the XGBoost model."""
        df = pd.DataFrame(model.feature_importances_, index=feature_names, columns=['importance'])
        df.sort_values(by='importance', ascending=False, inplace=True)
        df = df[:50]

        print(feature_names)
        plt.figure(figsize=(10, 8))
        sns.barplot(x=df['importance'], y=df.index , palette='viridis')
        plt.title('Feature Importance')     
        plt.savefig('images/feature_importance.svg')

    def plot_xgboost_tree(self, model):
        """Plot the first tree from the XGBoost model."""
        plt.figure(figsize=(20, 10))
        plot_tree(model, num_trees=0)

        plt.title('XGBoost Tree')
        plt.savefig('images/xgboost_tree.svg')


if __name__ == "__main__":
    # Example usage
    data_path = 'path/to/your/preprocessed_data.csv'
    #local testing for visualizer