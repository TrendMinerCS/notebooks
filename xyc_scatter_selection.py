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
url = 'https://my-server-url.trendminer.cloud/'
client = TrendMinerClient("{TM_TOKEN.password}", url)

# Loading TrendHub view: HEX data
from trendminer.views import Views

views = Views(client)
df = pd.concat(views.load_view('91b4922d-2128-42cc-96ac-904b61b4b209'))

# Choose the x and y tags, all other tags of the view can be selected as the color parameter
x_tag = 'TM-HEX-XI0620'
y_tag = 'TM-HEX-PI06202'
c_tags = list(df.columns)
c_tags.remove(x_tag)
c_tags.remove(y_tag)

import plotly.graph_objects as go
import plotly

fig = go.Figure()
fig.add_trace(go.Scatter(x=df[x_tag], y=df[y_tag], mode='markers', marker=go.scatter.Marker(color=df[c_tags[0]], colorscale='Viridis')))
    
buttons = [
    {
        'args': ['marker', go.scatter.Marker(color=df[tag], colorscale='Viridis')],
        'label': tag,
        'method': 'restyle'
    }
    for tag in c_tags]

fig.update_layout(
    updatemenus = [
        {
            'buttons': buttons,
            'direction': 'down',
            'pad': {"r": 10, "t": 10},
            'showactive': True,
            'x': 0.05,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }
        ]
    )
    
fig.update_layout(
    annotations = [
        {'text': 'parameter', 'showarrow': False, 'x': 0, 'y': 1.1, 'yref': 'paper', 'align': 'left', 'xref': 'paper'}
        ]
    )

html_str = plotly.io.to_html(fig, include_plotlyjs=True)
print("%html " + html_str)
