####################### ENTER INFORMATION BELOW ##################################

tm_url = '<TM_URL_HERE>'

#########################  ENTER INFORMATION ABOVE ################################


# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

from scipy import integrate
import scipy

import plotly.express as px
import plotly

# Loading TrendHub view: MonthlyStatistics
from trendminer.views import Views


# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}",tm_url)


####################### REPLACE VIEW UUID ##################################

views = Views(client)
df = views.load_view('653f5b4d-a763-4c66-9ae6-c6ce2cf08386')
df=pd.concat(df)

####################### REPLACE VIEW UUID ##################################


dfs = dict(tuple(df.groupby([df.index.month, df.index.year])))

ValueList=list()
TagList=list()
DateList=list()

for tag in df.columns:
    for i in dfs:
        y1 = np.array(dfs[i][tag])
        x1 = np.arange(len(dfs[i][tag]))
        R = round(scipy.integrate.trapz(y1,x1)/1440,1)
        ValueList.append(R)
        TagList.append(tag)
        DateList.append(i)
        

SummaryTable = pd.DataFrame({'month-year': DateList, 'tags': TagList, 'values': ValueList})
SummaryTable = SummaryTable.pivot(index='month-year', columns='tags', values='values')
SummaryTable['index']=SummaryTable.index
SummaryTable['index'] =  pd.to_datetime(SummaryTable['index'], format='(%m, %Y)')
SummaryTable = SummaryTable.set_index('index').sort_index()


df_formatted = SummaryTable.style.set_properties(**{'background-color': 'white'})

print("%html " + df_formatted.render())
print("%html " + plotly.io.to_html(px.line(SummaryTable)))
