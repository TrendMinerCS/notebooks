# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from datetime import timedelta

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient
from trendminer.views import Views

######################## ENTER INFORMATION BELOW #############################

myTZ = 'US/Central'
tm_url = 'https://dsitl-demo.trendminer.cloud/'

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", tm_url)

#Replace TrendHub view unique ID below
views = Views(client)
df = views.load_view('fe72c842-943c-4955-92ba-63cc5c2791e4')
df=df[0]

#Enter name of tag in dataframe that you wish to forecast
tagName = 'TM-T100-Ucoeff.PV_24hourAvg'

## Enter days of extrapolation and name of forecast feature
#Enter extrapolation in days
totalExtrapolation = 50

#Enter name of resulting "tag"
forecast_value_name = 'Forecast_U'

#Enter title for resulting graph
Name_of_parameter = "Heat Exchanger U Coefficient"


######################## ENTER INFORMATION ABOVE #############################


df.index = df.index.tz_convert(myTZ).tz_localize(None)

plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(14,6))

ax.plot(df.index, df[tagName], c='red')

#format plot
ax.set_title(Name_of_parameter, fontsize=24)
ax.set_xlabel('', fontsize=12)
fig.autofmt_xdate()
ax.set_ylabel(Name_of_parameter, fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=12)

df['dummy'] = df.index
df = df.reset_index(drop=True).reset_index()
print(df.dtypes)
print("%html " + df.head().style.render())


features = ["index"]
X = df[features]
y = df[tagName]

#Splitting the data using the train_test_split function.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50, shuffle=True)

# Define modeling steps and save into a pipeline
# This Pipeline function calls for a list of estimators and other operators in the form of tuples.
estimators = [('scaler', MinMaxScaler()),  #MinMaxScaler() is used to standardize the data
            ('model', LinearRegression())]

pipeline_obj = Pipeline(estimators)

#Training the model
model = pipeline_obj.fit(X_train, y_train)

FutureSteps = totalExtrapolation*1440/2
start = df['index'].max()
end = int(FutureSteps+len(df))


timestamp_list = np.linspace(df['index'].max(), (totalExtrapolation*1440/2+len(df)), (end-start+1), endpoint=True)
y_pred = model.predict(pd.DataFrame(timestamp_list)).tolist()
predicted_dataframe = pd.DataFrame(y_pred,index=timestamp_list)

new_df = pd.concat([predicted_dataframe, df], axis=1)
new_df = new_df.rename(columns = {0: forecast_value_name}, inplace = False)

FinalX = pd.date_range(start=new_df['dummy'][0], periods=len(new_df), freq='2T').to_pydatetime().tolist()

new_df['TS']=FinalX
new_df=new_df.set_index('TS')
new_df = new_df.drop(['index','dummy'], axis=1)

plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(16,4))

ax.plot(new_df.index, new_df[tagName], color='red')
ax.plot(new_df.index, new_df['Forecast_U'], color='blue', linestyle='--')

#format plot
ax.set_title(f"{Name_of_parameter} over {totalExtrapolation} days ", fontsize=24)
ax.set_xlabel('', fontsize=12)
fig.autofmt_xdate()
ax.set_ylabel(Name_of_parameter, fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=12)


