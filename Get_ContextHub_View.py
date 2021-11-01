####################### ENTER INFORMATION BELOW ##################################

### script will output a dataframe with plain format
### with all context item fields, startdate, endDate, keywords, description, itemtype, component and duration (minutes)

# 1) ******* Input <TM_URL> and ContextHub View ID

tm_url = '<TM_URL>'
viewID = '<ContextHub_ViewID>'

#########################  ENTER INFORMATION ABOVE ################################

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
import json
import datetime
import re

# Create TrendMiner API object
client = TrendMinerClient("{TM_TOKEN.password}", tm_url)

token = '{TM_TOKEN.password}'
auth_header    = {'Authorization':("Bearer " + token)}

#Get CH view information
endpoint = 'context/view/' + viewID + '/enriched'
r_context_view = requests.get(tm_url + endpoint, headers = auth_header)
r_context_view_json = r_context_view.json()

#Get number of pages of CH items
endpoint= "context/item/search?size=25"
body = {"filters": r_context_view_json['data']['filters']}
headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
r_context_item_pages = requests.post(tm_url + endpoint, headers=headers, json=body)
totalPages = r_context_item_pages.json()['page']['totalPages']

#For each page, get the all context items
endpoint= "context/item/search?size=25&page="
r_context_items_page_list = []
for i in range(1, totalPages+1, 1):
    r_context_items = requests.post(tm_url + endpoint + str(i), headers=headers, json=body)
    r_context_items_page_list.append(r_context_items.json()['content'])
    

#For each page in list, get context items and arrange in simple array
ContextItemList = []
for itemPage in r_context_items_page_list:
    for context_item in itemPage:
        (context_item['fields'])['startDate'] = context_item['events'][0]['occurred']
       
        if len(context_item['events']) != 2:
            (context_item['fields'])['endDate'] = ''    
        else:
            (context_item['fields'])['endDate'] = context_item['events'][1]['occurred']
        
        (context_item['fields'])['keywords'] = context_item['keywords']
        (context_item['fields'])['Description'] = context_item['description']
        (context_item['fields'])['ItemType'] = context_item['type']['name']
        (context_item['fields'])['Component'] = context_item['components'][0]['name']
        ContextItemList.append(context_item['fields'])


df = pd.DataFrame(ContextItemList)
df['TotalMinutes'] = (df['endDate'].astype('datetime64[ns]')-df['startDate'].astype('datetime64[ns]')).dt.total_seconds()/60
df['startDate'] = df['startDate'].astype('datetime64[ns]').dt.strftime("%m/%d/%Y %I:%M %p")
df['endDate'] = df['endDate'].astype('datetime64[ns]').dt.strftime("%m/%d/%Y %I:%M %p")
df = df.sort_values(by="startDate")
df=df.reset_index(drop=True)

#Printing the first 5 rows:
df_formatted = df.head().style.set_properties(**{'background-color': 'white'}).format({'TotalMinutes': "{:.2f}"})
print("%html " + df_formatted.render()) 
