# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

import os

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

# Create TrendMiner API object
client = TrendMinerClient(token, serverUrl)


serverUrl = os.environ["KERNEL_SERVER_URL"]

import requests
import json
import io

auth_header = {'Authorization': 'Bearer ' + token}

def get_context_item(key):
    response = requests.get(f"{serverUrl}/context/item/{key}", headers=auth_header)
    return response.json()

def get_attachment_links(links):
    for link in links:
        if link['rel'] == 'attachments':
            attachment_links = requests.get(link['href'], headers=auth_header).json()
            return attachment_links

def download_attachments(attachment_links):
    for attachment in attachment_links['content']:
        for link in attachment['links']:
            if link['rel'] == 'download':
                item_download_link = link['href']
                response = requests.get(item_download_link, headers=auth_header)
                #print(attachment['type'], '---', attachment['extension'], '----->', response)
                
                return response

#### ENTER CONTEXT ITEM ID HERE #####
my_key = "487-17"

item = get_context_item(my_key)

if item:
    attachment_links = get_attachment_links(item['links'])

    if attachment_links:
        file = download_attachments(attachment_links)
        
df = pd.read_csv(io.StringIO(file.text))

print(df)
