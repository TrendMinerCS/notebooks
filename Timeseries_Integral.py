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


SummaryTable = round(df.resample('M').apply(scipy.integrate.trapz)/1440,1)

df_formatted = SummaryTable.style.set_properties(**{'background-color': 'white'})

print("%html " + df_formatted.render())
print("%html " + plotly.io.to_html(px.bar(SummaryTable, orientation='v', opacity=0.6)))
