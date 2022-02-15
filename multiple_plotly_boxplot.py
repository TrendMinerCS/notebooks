# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

import plotly 
import plotly.graph_objects as go

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", "<ENTER_URL>")

df = pd.read_csv('https://raw.githubusercontent.com/TrendMiner/notebooks/main/data/parallel_coord.csv')

print(df.head())

#Data Preprocessing. Removing undefined phases and products.
df.drop(df[df['Phase_tag'] =="UNDEFINED"].index, inplace = True)
df.drop(df[df['Product_tag'] =="UNDEFINED"].index, inplace = True)

#Generating list of attributes that will be listed in the dropdown.
listColumns = list(df.columns)
listColumns.remove('Phase_tag')
listColumns.remove('Product_tag')

#Generating plot
fig = go.Figure()

# Adding 1 trace for each dropdown with any of the attributes (here I chose Conc_tag)
# One dropdown will display data vs Phase and the other vs Product.
# Add additional lines if looking to add 3rd or 4th dropdown.

fig.add_trace(go.Box(y=df['Conc_tag'], x=df['Phase_tag'], visible=True))
fig.add_trace(go.Box(y=df['Conc_tag'], x=df['Product_tag'], visible=False))


# Creating dropdown object and adding the rest of the attributes.
buttons1 = [dict(method = "restyle",
                 args = [{'x': [df['Phase_tag'], 'undefined'],
                          'y': [df[listColumns[k]], 'undefined'],
                          'visible':[True, False]}], 
                 label = listColumns[k])   for k in range(0, len(listColumns))] 

buttons2 = [dict(method = "restyle",
                 args = [{'x': ['undefined',df['Product_tag']],
                          'y': ['undefined', df[listColumns[k]]],
                          'visible':[False, True]}],
                 label = listColumns[k])   for k in range(0, len(listColumns))]


# Adjusting layout of the plot and position of the buttons. Add more buttons if necessary.
fig.update_layout(title_text='Plot Title',
                  title_x=0.4,
                  width=850,
                  height=450,
                  updatemenus=[dict(active=0,
                                    buttons=buttons1,
                                    x=1.15,
                                    y=1,
                                    xanchor='left',
                                    yanchor='top'),
                              
                               dict(buttons=buttons2,
                                    x=1.15,
                                    y=0.85,
                                    xanchor='left',
                                    yanchor='top')
                              ])


# Adding annotations to distinguish each button. Add more annotations if necesary.
fig.add_annotation(
            x=1.052,
            y=1,
            xref='paper',
            yref='paper',
            showarrow=False,
            xanchor='left',
            text="VS<br>PHASE")
fig.add_annotation(
            x=1.020,
            y=0.85,
            showarrow=False,
            xref='paper',
            yref='paper',
            xanchor='left',
            text="VS<br>PRODUCT");


print("%html " + plotly.io.to_html(fig, include_plotlyjs=True))
