from datawrangler import DataWrangler
from model import Model
import os
from visualizer import Visualizer

# Final script to run the entire pipeline
data_path = 'data/job_posting_data.csv'
wrangler = DataWrangler(data_path)
v = Visualizer()
df = wrangler.clean_data()

model = Model()
model.train_model(df)
model.save_model("model.pkl")

v.plot_xgboost_importance(model.model, model.model_columns)
v.plot_xgboost_tree(model.model)