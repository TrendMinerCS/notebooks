# Necessary packages
import plotly.graph_objects as go
import plotly
import os
import time

# Your trendminer url:
url = "https://my-trendminer-server.trendminer.cloud/"

# Set filename and desired refresh rate
filename = 'cached_plotly_output.html'
refresh_rate = 3600 #in seconds

# if the file does not exist, or is older than the refresh rate, execute the code
if not os.path.exists(filename) or (time.time() - os.stat(filename).st_mtime > refresh_rate):
    
    # Update existing file edit date to prevent parallel calculations
    with open(filename, 'a') as f:
        f.write(' ')
    
    # package imports
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    # TrendMiner package import
    import trendminer
    from trendminer.trendminer_client import TrendMinerClient

    # Create TrendMiner API object
    client = TrendMinerClient("{TM_TOKEN.password}", url)
    
    from trendminer.views import Views
    views = Views(client)
    
    # Load data from saved views
    
    df1 = views.load_view('cb3a8654-86a8-44e1-88dd-34e5dacc208f')
    df1 = pd.concat(df1)
    
    df2 = views.load_view('7a2f3632-4f1c-401a-9068-ca8cc5a8c5ef')
    df2 = pd.concat(df2)
    
    
    # List of columns
    cols1 = df1.columns
    cols2 = df2.columns
    
    # Creating figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1.index, y=df1[cols1[0]]))
    fig.add_trace(go.Scatter(x=df2.index, y=df2[cols2[0]], visible=False))
    
    #The trace restyling  to be performed at an option selection in the first/second dropdown menu
    # is defined within  buttons1/buttons2 below:
    buttons1 = [dict(method = "restyle",
                     args = [{'x': [df1.index, 'undefined'],
                              'y': [df1[cols1[k]], 'undefined'],
                              'visible':[True, False]}], 
                     label = cols1[k])   for k in range(0, len(cols1))]  
    
    buttons2 = [dict(method = "restyle",
                     args = [{'x': ['undefined', df2.index],
                              'y': ['undefined', df2[cols2[k]]],
                              'visible':[False, True]}],
                     label = cols2[k])   for k in range(0, len(cols2))]
    
    fig.update_layout(title_text=f'Plot Title ({datetime.fromtimestamp(time.time()).strftime("%h %d %H:%M")})',
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
    
    #Add annotations for the two dropdown menus:
    fig.add_annotation(
                x=1.065,
                y=1,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='left',
                text="df1<br>Name")
    fig.add_annotation(
                x=1.065,
                y=0.85,
                showarrow=False,
                xref='paper',
                yref='paper',
                xanchor='left',
                text="df2<br>Name");
                
    
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ]),
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )
            
    html_str = plotly.io.to_html(fig, include_plotlyjs=True)
    
    with open(filename, 'w') as f:
        f.write(html_str)

# The file exists and is up to date
else:
    with open(filename, 'r') as f:
        html_str = f.read()

# create the output    
print("%html " + html_str)
