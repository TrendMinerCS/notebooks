# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", '<ENTER_TRENDMINER_URL>')

# Loading TrendHub view: BA views
# ******** LOAD TRENDHUB VIEW WITH OPTIMAL/IDEAL OPERATING CONDITIONS *************
from trendminer.views import Views

views = Views(client)
# Modify viewID and tag names below.
df = views.load_view('3449b421-c150-4889-923c-efed478d499e')
selection = ['BA:CONC.1', 'BA:TEMP.1', 'BA:LEVEL.1']

# concatenate and show the data
df_train = pd.concat(df)
z.show(df_train)

# train built-in anomaly model
from trendminer_experimental.anomaly_detection.model import TMAnomalyModel
model = TMAnomalyModel()
q_error, topo_error = model.fit(df_train[selection], 1000)

# plot error
plt.plot(q_error)
plt.plot(topo_error)

# Publish the model
# ************* NAME THE MODEL ********************
model_name = 'TMAnomaly_BA'

from trendminer.ml.models import ZementisModels
from pprint import pprint
zementis = ZementisModels(client)


# Remove existing model if present
try:
    zementis.delete_model(model_name)
except trendminer.ml.models.exceptions.MLModelNotFoundException:
    pass

model_pmml = model.to_pmml(model_name, threshold_percentage=0.95)

#replace variable names
for i, s in enumerate(selection):
    model_pmml = model_pmml.replace(f'Variable_{i}', s)

model_id = zementis.deploy_model(model_pmml)

pprint(zementis.model_details(model_id))
