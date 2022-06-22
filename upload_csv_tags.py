import pandas as pd
import numpy as np
import requests

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

import trendminer
from trendminer.trendminer_client import TrendMinerClient

url = "https://dsitl-demo.trendminer.cloud"

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", url)


# Functions
def structure_csv(df, names, descriptions, units, types, prefix=None):
  """Structure dataframe to right multi-header format for csv upload"""
    if prefix is None:
        prefix = ""

    df.fillna("", inplace=True)

    def insertcolon(timestring):
        return timestring[0:-2] + ":" + timestring[-2:]

    if df.index.tz is None:
        df.index = df.index.tz_localize("utc")

    df.index = df.index.strftime("%Y-%m-%dT%H:%M:%S%z").map(insertcolon)

    df.columns = pd.MultiIndex.from_tuples(
        zip(
            names,
            descriptions,
            units,
            types,
        )
    )

    return df
    
    
def upload_df(df):
  """Upload data to csv endpoint through post request"""
    token = "{TM_TOKEN.password}"
    headers = {'Authorization': f'Bearer {token}'}
    tagdata = df.to_csv(index_label=False)
    files = {"file": ("tagdata.csv", tagdata)}
    requests.post(url=f"{url}/ds/imported/timeseries/",files=files, headers=headers)


# Loading TrendHub view: QSS
from trendminer.views.views import Views
views = Views(client)
df = views.load_view('1ba04bf3-65dc-4560-8378-23f834b8f02f')[0]


# Structure view to right format for csv upload
names = ['csv_labdata', 'csv_flow', 'csv_temp']
descriptions = names
units = ['', 'm3/h', 'C']
types = ['discrete', 'analog', 'analog']
df_upload = structure_csv(df, names=names, descriptions=descriptions, units=units, types=types)


# Upload as new csv tags
upload_df(df_upload)

