# LOAD DATA
import os
import pandas as pd

import trendminer
from trendminer.trendminer_client import TrendMinerClient
from trendminer.views.views import Views

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

client = TrendMinerClient(token, serverUrl)
views = Views(client)

# Load heat exhanger data
df = pd.concat(views.load_view('eb8b8c2f-dcb5-43a8-9fc2-39c4dc4e7905'))

df.head()


# FIT MODEL
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


y = df["TM-T200-FI251.PV"]
X = df.loc[:, ["TM-T200-FI201.PV", "TM-T200-TI201.PV", "TM-T200-TI251.PV"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=15)

pipeline = Pipeline([('scaler', StandardScaler()),  # standardize the input
                         ('model', LinearRegression())]) # Predict using SVC

pipeline.fit(X_train, y_train)

plt.plot(pipeline.predict(X_test), y_test.values, ".")

print(f"R2 score: {r2_score(y_test, pipeline.predict(X_test))}")


# PUBLISH MODEL
from trendminer.ml.models import ZementisModels
from nyoka import skl_to_pmml

models = ZementisModels(client)

# Save model to pmml file
model_name = "T200_heating_flow"

skl_to_pmml(pipeline=pipeline, # our pipeline object
            col_names=["product flow", "product temp", "heating water temp"], # the names of our input variables
            target_name="heating water flow", # the name(s) of our output variable(s)
            pmml_f_name=f"{model_name}.pmml", # name of the output pmml file
            model_name=model_name,
            description="Predicts heating water flow through linear regression")

# Read the model from the saved file
with open(f"{model_name}.pmml", 'r') as f:
    model_string = f.read()

# Delete the model if it already exists to enable saving the new version
try:
    models.delete_model(model_name)
except trendminer.ml.models.exceptions.MLModelNotFoundException:
    pass

# Save the model
models = ZementisModels(client)
model_id = models.deploy_model(model_string)

# Display model details
models.model_details(model_id)
