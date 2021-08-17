# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

import requests
import io
import json
import statistics as stats


# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}")

#--------------------LOADING DATA FROM GITHUB-------------------------

url = 'https://raw.githubusercontent.com/TrendMiner/notebooks/main/data/quality_data.csv'
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))

#--------------------LOADING DATA FROM GITHUB-------------------------

# The historical mean for the process variable in question
process_mean = stats.mean(df['y'])

# The historical standard variation for the process variable in question
process_stddev = stats.stdev(df['y'])

# Process data
process_data = df['y']


# Plot the XBar chart
fig, ax = plt.subplots(figsize = (10, 6))

# Create the XBar chart
ax.plot(process_data, linestyle='-', marker='o', color='blue')

# Create the Upper Control Limit Line
UCL = process_mean + 3 * process_stddev
ax.axhline(UCL, color='red')

# Create the Lower Control Limit Line
LCL = process_mean - 3 * process_stddev
ax.axhline(LCL, color='red')

# Create the Xbar line
ax.axhline(process_mean, color='green')

# Create a chart title
ax.set_title('SPC Chart')

# Label the axes
ax.set(xlabel='Sample', ylabel='Mean')

# Determine the x-axis limits in the chart to attach reference values
left, right = ax.get_xlim()
ax.text(right + 0.3, UCL, "UCL = " + str("{:.2f}".format(UCL)), color='red')
ax.text(right + 0.3, process_mean, r'$\bar{x}$' + " = " + str("{:.2f}".format(process_mean)), color='green')
ax.text(right + 0.3, LCL, "LCL = " + str("{:.2f}".format(LCL)), color='red')

plt.show()
