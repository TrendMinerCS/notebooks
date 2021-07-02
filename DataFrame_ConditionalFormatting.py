# This script shows how to format a row based on a value/string of a specific column
# and formatting a single column based on the value of that column.
# and formatting a single column based on the value of another column

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
client = TrendMinerClient("{TM_TOKEN.password}")

#### Conditional Formatting #####
import pandas as pd
import datetime

ListOfDictionaries = {
        'Reactor Type' : ['Reactor1', 'Reactor1', 'Reactor2', 'Reactor1', 'Reactor2','Reactor2', 'Reactor5'],
        'Viscosity' : [34, 30, 16, 23, 12, 8, 3],
        'Sample Date' : ['2/3/2020 21:03', '2/4/2020', '2/3/2020 08:02', '2/6/2020', '2/3/2020', '2/9/2020', '1/9/2020']
    }
    
df =  pd.DataFrame(ListOfDictionaries)
df['Sample Date'] = df['Sample Date'].astype('datetime64[ns]').dt.strftime("%B %d, %Y at %I:%M %p")
df = df.sort_values(by="Sample Date").reset_index(drop=True)


# Format a row based on the value of a column (Formatting the row based on Reactor Type)
def FormatRows(row):
    reactor1 = 'background-color: pink'
    reactor2 = 'background-color: lightblue'
    other = ''
    
    if row['Reactor Type'] == 'Reactor1':
        return [reactor1] * len(row)
    elif row['Reactor Type'] == 'Reactor2':
        return [reactor2] * len(row)
    else:
        return [other] * len(row)
        
    
# Format a cell based on the value of that same cell (Formatting Viscosity based on its value)
def FormatValue(cell):    
    highlight = 'color: red;'
    default = 'color: green'

    if cell['Viscosity'] >= 16:
        return [highlight]
    else:
        return [default]
        
      
# Format a cell based on the value of that same cell (Formatting Sample Date based on Viscosity)
def FormatDifferentValue(cell):    
    highlight = 'color: blue;'
    default = 'color: orange'
    blank = ''

    if cell['Viscosity'] >10 :
        return [blank,highlight]
    else:
        return [blank,default]
        


df_formatted= df.style.apply(FormatRows, axis=1).apply(FormatValue, subset=['Viscosity'], axis=1).apply(FormatDifferentValue, subset=['Viscosity', 'Sample Date'], axis=1)
print("%html " + df_formatted.render()) 
