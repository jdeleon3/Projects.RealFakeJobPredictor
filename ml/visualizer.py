import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_histogram(self):
        """Plot histograms for each numerical column."""
        pass

    

if __name__ == "__main__":
    # Example usage
    data_path = 'path/to/your/preprocessed_data.csv'
    #local testing for visualizer