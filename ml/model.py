import pandas as pd
import numpy as np
import os
import pickle
from textclassifier import TextClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
from visualizer import Visualizer


class Model:
    def __init__(self):        
        self.text_classifier = TextClassifier()
        self.model = XGBClassifier()
        self.model_columns = []
        self.v = Visualizer()
        

    def train_model(self, df: pd.DataFrame):
        """
        Train the model using the provided DataFrame.
        df: pd.DataFrame: The DataFrame containing job descriptions and their corresponding labels.
        """
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or not provided.")
        
        # Split the data into training and testing sets
        X = df['description']
        y = df['fraudulent']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
                
        # Transform the training and testing data
        X_train_transformed = self.text_classifier.fit_transform(X_train)
        X_test_transformed = self.text_classifier.transform(X_test)
        self.model_columns = X_train_transformed[1]
        # Train the model
        self.model.fit(X_train_transformed[0], y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test_transformed[0])
        self.v.plot_confusion_matrix(y_test, y_pred, labels=[0, 1])
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    def predict(self, data):
        """
        Predict the label for the provided data.
        data: str: The job description to predict.
        """
        if not isinstance(data, str):
            raise ValueError("Input must be a string.")
        
        # Transform the input data
        data_transformed = self.text_classifier.transform([data])
        
        # Make prediction
        prediction = self.model.predict(data_transformed)
        
        return prediction[0]

    def save_model(self, filename="model.pkl"):
        """Save the model to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)
        with open("text_classifier.pkl", 'wb') as f:
            pickle.dump(self.text_classifier, f)
        print(f"Model saved to {filename}")

    def load_model(self, filename="model.pkl"):
        """Load the model from a file."""
        if not filename.endswith('.pkl'):
            raise ValueError("Filename must end with '.pkl'")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' does not exist.")
        
        with open(filename, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {filename}")

if __name__ == "__main__":
    from datawrangler import DataWrangler
    # Example usage
    data_path = 'data/job_posting_data.csv'
    wrangler = DataWrangler(data_path)
    df = wrangler.clean_data()
    model = Model()
    model.train_model(df)
    model.save_model("model.pkl")
