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

import requests
import json

auth_header = {'Authorization': 'Bearer ' + token}


def get_contextItem_attachment(attachmentEndpoint):
    
    r = requests.get(f'{serverUrl}/context{attachmentEndpoint}', headers=auth_header)
        
    return r
  
  
attachmentEndpoint = "/data/046cb744-3690-4a32-8c9c-e171cb906066/attachments/d153bee5-cc86-4546-a217-423eb26bb024/download"

r = get_contextItem_attachment(attachmentEndpoint)

## "r" contains the attachment object. Depending on the format of the file, you might have to take additional actions afterwards to convert to the proper format.
