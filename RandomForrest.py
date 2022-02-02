############################ INPUTS #########################

tm = "TM_URL"
training_view_id = "TM_UUID"

model_name = "R101Pressure_RandomForest"
pmml_file = "R101_RandForest.pmml"
target_name="R101_Pressure"

############################ INPUTS #########################

# Suggested data science package imports
import pandas as pd
import numpy as np
from datetime import datetime

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

# Machine Learning packages
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import max_error


#Plotting packages
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as style

import plotly.express as px
import plotly.graph_objects as go
import plotly

import warnings
warnings.filterwarnings("ignore")

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", tm)


from trendminer.views.views import Views

views = Views(client)
df = views.load_view(training_view_id)   ########### Training view with Xs and Ys
df_train = pd.concat(df)


features = ["R101_FI1", "R101_FI2"] ###################### define model features (Xs)
X = df_train[features]
y = df_train["R101_PI"]             ###################### Variable of interest (Y)

#Splitting the data using the train_test_split function.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)


'''
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

grid_params = {
 'n_estimators' : [5,10,50,100,200],
 'max_features' : ['auto', 'sqrt', 'log2'],
 'max_depth' : [4,5,6,7,8],
 'bootstrap' : [True, False]
}


optimizedModel = GridSearchCV(RandomForestRegressor(), grid_params, cv=5, n_jobs=-1, verbose=1).fit(X_train, y_train)
print('Best hyper parameter (GRID SEARCH):')
print(optimizedModel.best_params_)
'''


estimators = [('model', RandomForestRegressor(bootstrap=True, max_depth=8, max_features='auto', n_estimators=200))]
pipeline_obj = Pipeline(estimators)
myModel = pipeline_obj.fit(X_train, y_train)


y_pred = myModel.predict(X_test)

print("MSE = ", "{:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Max Error = ", "{:.3f}".format(max_error(y_test, y_pred)))
print("Mean Abs Error = ", "{:.3f}".format(mean_absolute_error(y_test, y_pred)))

importance = [(feature, imp) for feature, imp in(
    myModel[0].feature_importances_, features)]

print(importance)


from nyoka import skl_to_pmml

#Converting model to pmml
skl_to_pmml(pipeline=myModel,
            col_names=features,
            target_name=target_name,
            pmml_f_name=pmml_file,
            model_name=model_name,
            description="description")


from trendminer.ml.models import ZementisModels

#Deploying model with Zementis
with open(pmml_file,"r") as f:
    string = f.read()

# But first, lets delete the model from pervious demo
zementis = ZementisModels(client)
try:
    zementis.delete_model(model_name)
except trendminer.ml.models.exceptions.MLModelNotFoundException:
    pass

# Now we can deploy the model and voila!
models = ZementisModels(client)
model_id = models.deploy_model(string)
model_details = models.model_details(model_id)


from plotly.subplots import make_subplots
import plotly.graph_objects as go

data = {'features':features, 'importance':myModel[0].feature_importances_.tolist()}
importance_matrix = pd.DataFrame(data).set_index('features')

importance_matrix=importance_matrix.sort_values(by='importance', ascending=False)
importance_matrix['cumulative importance']=importance_matrix['importance'].cumsum()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(x=importance_matrix.index, y=importance_matrix['importance'], name="importance"), secondary_y=False)
fig.add_trace(go.Scatter(x=importance_matrix.index, y=importance_matrix['cumulative importance'], name="cumulative imp."), secondary_y=True)
fig.update_layout(title_text="Loss Points Random Forest", autosize=True)#width=620, height=500)

print("%html " + plotly.io.to_html(fig, include_plotlyjs=True))
