# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

import plotly
import seaborn as sns
import plotly.express as px

import trendminer
from trendminer.trendminer_client import TrendMinerClient

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", '<TM_URL>')

# Create the chart:
DataFrame = pd.read_csv('https://raw.githubusercontent.com/TrendMiner/notebooks/main/data/parallel_coord.csv')
fig = px.parallel_coordinates(DataFrame, dimensions=DataFrame.columns.tolist(), color='TM-BP2-PRODUCT.1')

# Show the plot
print("%html " + plotly.io.to_html(fig, include_plotlyjs=True))
