import pandas as pd
from pprint import pprint

from datetime import datetime, timedelta
from dateutil import parser

import plotly.graph_objects as go
import plotly
import os
import time
import requests

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient
from trendminer.ml.models import ZementisModels

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

# Create TrendMiner API object
client = TrendMinerClient(token, serverUrl)
models = ZementisModels(client)

# This is the key of the context item on which we will save our attachments
context_item_key = "41F-09"

r = requests.get(f"{os.environ['KERNEL_SERVER_URL']}/context/item/{context_item_key}",
                headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"}) 

context_item_identifier = r.json()["identifier"]

# Extract context item attachment data
response = requests.get(
    f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item_identifier}/attachments",
    headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"},
    params={"size": 1000})


for data in response.json()["content"]:
    
    if f"{data['extension']}" != "pmml":
        continue
        
    attachment_id = data["identifier"]
    
    file_name = data["name"]
    
    r = requests.get(
        f"{os.environ['KERNEL_SERVER_URL']}/context/data/{context_item_identifier}/attachments/{attachment_id}/download",
        headers={"Authorization": f"Bearer {client._TrendMinerClient__token}"},
        )
    
    model_string = r.content
    model_name = file_name
    
    # Delete the model if it already exists to enable saving the new version
    try:
        models.delete_model(model_name)
    except trendminer.ml.models.exceptions.MLModelNotFoundException:
        pass
    
    # Save the model
    models = ZementisModels(client)
    model_id = models.deploy_model(model_string)
    
    # Display model details
    print(f"--- {model_name} ---")
    pprint(models.model_details(model_id))
    print("\n\n")
