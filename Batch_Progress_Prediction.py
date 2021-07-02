# Suggested data science package imports
import pandas as pd
import numpy as np
from pprint import pprint

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", '<ENTER_TRENDMINER_URL>')

# Loading TrendHub view: BA views
from trendminer.views import Views

views = Views(client)
# Replace TrendHub view unique ID
df = views.load_view('3449b421-c150-4889-923c-efed478d499e')

# Add progress variable
for idf in df:
    idf['progress'] = np.linspace(0,100,len(idf))

df[0].plot()

df = pd.concat(df)
df.drop('BA:ACTIVE.1', axis=1, inplace=True)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from trendminer.ml.models import ZementisModels
from nyoka import skl_to_pmml

target = ['progress']

#Replace tag names below...
numeric_features = ['BA:LEVEL.1', 'BA:CONC.1', 'BA:TEMP.1']
    
clf = Pipeline(steps=[
    ('preprocessor', PolynomialFeatures(degree=3)),
    ('scaler', MinMaxScaler()),
    ('model', LinearRegression())])
    
xtrain, xtest, ytrain, ytest = train_test_split(df[numeric_features], df[target], test_size=0.2, random_state=0)

clf.fit(xtrain, ytrain)

predicted_y = clf.predict(xtest)

plt.scatter(ytest, predicted_y)

print(r2_score(ytest, predicted_y))

model_name = 'BA_Progress'

filename = f'{model_name}.pmml'

skl_to_pmml(pipeline=clf, pmml_f_name=filename, col_names=xtrain.columns.tolist(), target_name=ytrain.columns[0], model_name=model_name, description='BA batch progress variable')

with open(filename, 'r') as f:
    model_string = f.read()
    
zementis = ZementisModels(client)

# Remove existing model if present
try:
    zementis.delete_model(model_name)
except trendminer.ml.models.exceptions.MLModelNotFoundException:
    pass

model_id = zementis.deploy_model(model_string)

print(zementis.model_details(model_id))
