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
client = TrendMinerClient("{TM_TOKEN.password}", '<ENTER_URL>')

try:
    length = z.input("Enter minutes: ")

    if int(length) <= 0:
        length = '1'

    from trendminer.views import Views
    
    views = Views(client)
    df = views.load_view('<ENTER_VIEW_ID>')
    df = pd.concat(df)
    
    df2 = df.tail(int(length))
    
    
    #print(df.columns) # Remove comment hash to see tags available in dataframe
    x = 'NAME_OF_TAG_ON_X_AXIS' # Define dataframe column / tag for x axis
    y = 'NAME_OF_TAG_ON_Y_AXIS' # Define dataframe column / tag for y axis
    
    
    plt.scatter(x = df[x], y = df[y]+0.9, c=df.index, cmap='Blues', s=100, alpha=0.80)
    plt.scatter(x = df2[x], y = df2[y]+0.9, c='red',  s=100, edgecolors = 'black')
    plt.title(y + ' vs. ' + x, size = 20)
    plt.xlabel(x, size = 12)
    plt.ylabel(y, size = 12)
    
except ValueError:
    print("Oops! That was not a valid number. Try again...")


plt.show()

print("\nRefresh dashboard to change time frame...")
