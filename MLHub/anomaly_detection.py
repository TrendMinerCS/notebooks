import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

from trendminer.trendminer_client import TrendMinerClient
from trendminer.views.views import Views
from trendminer_experimental.anomaly_detection.model import TMAnomalyModel

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

client = TrendMinerClient(token, serverUrl)
views = Views(client)

# Loading normal data
df_list = views.load_view('2ad12a92-7590-40b8-b674-73637649cf5b')

# Concat the views 
df = pd.concat(df_list)

# Limit the selection, take only 1 in 6 points
df_train = df.iloc[0::6,:]


model = TMAnomalyModel()
q_error, topo_error = model.fit(df_train, 1000)

# Plot errors
plt.plot(q_error)
plt.plot(topo_error)

model = TMAnomalyModel()
q_error, topo_error = model.fit(df_train, 1000)

# Publish the model
from trendminer.ml.models import ZementisModels
from pprint import pprint

# Enter model name. No spaces
model_name = "ENTER_YOUR_MODEL_NAME"

models = ZementisModels(client)

# Delete existing model if present
try:
    models.delete_model(model_name)
except trendminer.ml.models.exceptions.MLModelNotFoundException:
    pass

model_pmml = model.to_pmml(model_name, threshold_percentage=0.9)

# Replace variable names
for i, s in enumerate(df_train.columns):
    model_pmml = model_pmml.replace(f"Variable_{i}", s)

model_id = models.deploy_model(model_pmml)
model_details = models.model_details(model_id)

pprint(model_details)
