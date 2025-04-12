import pandas as pd
import numpy as np
import os
import pickle


class Model:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        

    def train_model(self):
        pass

    def predict(self, data):
        pass

    def save_model(self, filename="model.pkl"):
        """Save the model to a file."""
        pass

if __name__ == "__main__":
    import DataWrangler 
    # Example usage
    data_path = 'data/job_posting_data.csv'
    wrangler = DataWrangler(data_path)

    m = Model(df=wrangler.df)

