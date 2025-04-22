import pandas as pd
import numpy as np
import os

class DataWrangler:

    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        """Load data from a CSV file."""
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            print(f"Data loaded successfully from {self.data_path}.")
        else:
            raise FileNotFoundError(f"The file {self.data_path} does not exist.")

    def clean_data(self):
        """Clean the dataset by removing duplicates and handling missing values."""
        if self.df is not None:
            initial_shape = self.df.shape
            self.df.drop_duplicates(inplace=True)
            self.df.dropna(inplace=True)
            final_shape = self.df.shape
            print(f"Data cleaned: {initial_shape} -> {final_shape}")
            return self.df
        else:
            raise ValueError("Data not loaded. Please load the data first.")
        
if __name__ == "__main__":
    # Example usage
    data_path = 'data/job_posting_data.csv'
    wrangler = DataWrangler(data_path)
    
    try:
        wrangler.load_data()
        wrangler.clean_data()
    except Exception as e:
        print(f"An error occurred: {e}")