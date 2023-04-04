import pandas as pd

from datetime import datetime, timedelta
from dateutil import parser

import plotly.graph_objects as go
import plotly
import os
import time
import requests
import pytz

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

# Create TrendMiner API object
client = TrendMinerClient(token, serverUrl)

# Set filename and desired refresh rate
filename = 'cached_plotly_output.json'
refresh_rate = timedelta(seconds=3600)

# This is the identifier of the context item on which we will save our attachments
# To get identifiers: right click in the browser > inspect > Open 'Network' tab > click context item > extract id from request url
context_item = "269a22f6-5198-4177-be8c-781389139624"

# Get current time
current_time = pytz.utc.localize(datetime.utcnow())

# Extract context item attachment data
response = requests.get(
    f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item}/attachments",
    headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"},
    params={"size": 1000})

exists = False
for data in response.json()["content"]:
    if f"{data['name']}.{data['extension']}" == filename:
        exists = True
        creation_time = parser.isoparse(data["lastModifiedDate"])
        attachment_id = data["identifier"]
        break

# if the file does not exist yet, or is older than the refresh rate, execute the code
if not exists or ((creation_time + refresh_rate) < current_time): 
    # Update existing file edit date to prevent parallel calculations
    with open(filename, 'a') as f:
        f.write(' ')
    
    from trendminer.views.views import Views
    views = Views(client)
    
    # Load data from saved views
    df_list = views.load_view('eb8b8c2f-dcb5-43a8-9fc2-39c4dc4e7905')
    df1 = df_list[0]
    df2 = df_list[1]
    
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
    
    fig.update_layout(title_text=f'Data from {creation_time.strftime("%h %d %H:%M")} UTC',
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

    # Remove old file    
    if exists:
        r = requests.delete(
                f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item}/attachments/{attachment_id}",
                headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"},
            )
        r.raise_for_status()
    
    # Save new file
    name, extension = filename.split(".")
    r = requests.post(
            f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item}/attachments",
            headers={
                "Authorization": f"Bearer {client._TrendMinerClient__token}",
                #"accept": "*/*",
                "content-type": "application/octet-stream",
            },
            files={"file": (filename, plotly.io.to_json(fig))},
            params={
                "name": name,
                "extension": extension,
            }
        )
    r.raise_for_status()

# The file exists and is up to date
else:
    r = requests.get(
        f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item}/attachments/{attachment_id}/download",
        headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"},
        )
    
    # split off the metadata from the actual content, might need some finetuning depending on the file type
    json_str = str(r.content).split("\\r\\n")[3]
    fig = plotly.io.from_json(json_str)
        
fig
