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

# # # # # # # # # # # # MODIFY CONTEXT_ITEM ID AND DATA BELOW # # # # # # # # # # # # # # # # # # # 

context_item = '228173ad-d8b8-40cf-8b0b-29abaedf26c1'

# Generate some data to plot
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

dt_string = (datetime.now()).strftime("%d-%m-%Y--%H-%M-%S")

extension = 'pdf'
pdf_filename = f'daily-report-date-{dt_string}.{extension}'
name, extension = pdf_filename.split(".")

# Create a Matplotlib figure
fig, ax = plt.subplots()
ax.plot(x, y)

# Save the figure to a PDF file
plt.savefig(pdf_filename, format=extension)

try:
    files = {'file': (pdf_filename, open(pdf_filename, 'rb'), f'application/{extension}')}
    os.remove(pdf_filename)
    auth_header = {'Authorization':("Bearer " + token), 'Content-type':'application/octet-stream'}
    r = requests.post(f"{serverUrl}/context/data/{context_item}/attachments", headers=auth_header, files=files, params={"name": name, "extension": extension})
except:
    print(f"File '{pdf_filename}' does not exist.")
