# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt


import os

serverUrl = "ENTER URL HERE"


from datetime import timedelta
import requests
import json
import time
import pytz




"### TOKEN FUNCTION GOES HERE"

auth_header = {'Authorization': f'Bearer {token}'}

def value_search_and_calculations(startDate, endDate, conditions, minDuration, operator, calculations):
    
    if minDuration < int((requests.get(url=f'{serverUrl}/ds/configurations/INDEX_RESOLUTION', headers=auth_header)).json()['value'])*2:
        raise ValueError("minDuration must be at least 120 seconds (i.e. twice the indexing resolution; Note: changing indexing resolution will delete all the indexes")
    
    request_body= {
      "contextTimePeriod": {
        "startDate": startDate,
        "endDate": endDate
      },
      "definition": {
        "type": "VALUE_BASED_SEARCH",
        "queries": conditions,
        "parameters": {
          "minimumDuration": minDuration,
          "operator": operator
        },
        "calculations": calculations
      }
    }

    r = requests.post(url=f'{serverUrl}/compute/search-requests', json=request_body, headers=auth_header)
    
    return r.json()


def get_tag_details(tagname):
    
    params = {'tagName': tagname}
    
    r = requests.get(f'{serverUrl}/hps/api/tags/details', params=params, headers=auth_header)
        
    return r

    
def search_calcs_results_status(requestID):

    r = requests.get(url=f'{serverUrl}/compute/search-requests/{requestID}', headers=auth_header)
    
    return r.json()


def search_calcs_results(requestID, page, size):

    r = requests.get(url=f'{serverUrl}/compute/search-requests/{requestID}/results?page={page}&size={size}', headers=auth_header)
    
    return r.json()
  
  
# start and end date over which you wan to perform the search:

#################### CONFIGURATION ####################

start = datetime(2022, 3, 5, 0, 0, 0)
end = datetime(2022, 5, 13, 0, 0, 0)
target_timezone = 'US/Eastern'

timezone = pytz.timezone(target_timezone)
start += timedelta(hours=int(timezone.utcoffset(start).total_seconds() / 3600 * -1))
end += timedelta(hours=int(timezone.utcoffset(end).total_seconds() / 3600 * -1))
startDate = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
endDate = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')


EventDefinitions = {
    "Water Rinse Phase": {
        "minDuration" : 120, #seconds
        "search_conditions" : [
            {
                "reference": {"name": "[F&B]B_XV3093_CIP.PV", "shift": 0},
                "condition": "=", "values": [1]
            }
        ],
        "operator": "AND",
        "search_calculations" : []
    },
    
    "Acid Rinse Phase": {
        "minDuration" : 120,
        "search_conditions" : [
            {
                "reference": {"name": "[F&B]B_XV3093_CIP.PV", "shift": 0},
                "condition": "=", "values": [2]
            }
        ],
        "operator": "AND",
        "search_calculations" : []
    },
    
    "Caustic Rinse Phase": {
        "minDuration" : 120,
        "search_conditions" : [
            {
                "reference": {"name": "[F&B]B_XV3093_CIP.PV", "shift": 0},
                "condition": "=", "values": [3]
            }
        ],
        "operator": "AND",
        "search_calculations" : []
    },
    
    "UPW Rinse Phase": {
        "minDuration" : 120,
        "search_conditions" : [
            {
                "reference": {"name": "[F&B]B_XV3093_CIP.PV", "shift": 0},
                "condition": "=", "values": [4]
            }
        ],
        "operator": "AND",
        "search_calculations" : []
    },
    
    "Batch Cycle": {
        "minDuration" : 120,
        "search_conditions" : [
            {
                "reference": {"name": "[F&B]B_XV3092_Production.PV", "shift": 0},
                "condition": "=", "values": [1]
            }
        ],
        "operator": "AND",
        "search_calculations" : []
    }
}


for eventDefinition in EventDefinitions:
    for condition in EventDefinitions[eventDefinition]['search_conditions'][:]:
        try:
            r = get_tag_details(condition['reference']['name'])
            r.raise_for_status()
            condition['reference']['interpolationType'] = r.json()['interpolationType']

        except:
            search_conditions.remove(condition)
            print(condition['reference']['name'], ' not found')
            
# Filling in the missing key:values for the search_calculations
for eventDefinition in EventDefinitions:
    for calc in EventDefinitions[eventDefinition]['search_calculations'][:]:
        r = get_tag_details(calc['reference']['name'])
        if r.status_code == 200:  
            calc['reference']['id'] = r.json()['id']
            calc['reference']['interpolationType'] = r.json()['interpolationType']
        else:
            search_calculations.remove(calc)
            
 for eventDefinition in EventDefinitions:    
    if len(EventDefinitions[eventDefinition]['search_conditions']) > 0:

        search_conditions = EventDefinitions[eventDefinition]['search_conditions']
        minDuration = EventDefinitions[eventDefinition]['minDuration']
        operator = EventDefinitions[eventDefinition]['operator']
        search_calculations = EventDefinitions[eventDefinition]['search_calculations']
        
        r_search_calcs = value_search_and_calculations(startDate, endDate, search_conditions, minDuration, operator, search_calculations)
        
        requestID = r_search_calcs['id']

        # Waiting a few seconds to generate results (do not change this)
        time.sleep(3)
        r_search_calcs_status = search_calcs_results_status(requestID)

        # Looping through request until search results and calculations are generated in TrendMiner
        while r_search_calcs_status.get('status') != 'DONE':
            time.sleep(3)
            r_search_calcs_status = search_calcs_results_status(requestID)

        r_search_calcs_results = search_calcs_results(requestID, 0, size = 1000)

        all_content = []
        all_content.extend(r_search_calcs_results['content'])


        # Loop through each page in the response
        for i in range(1, r_search_calcs_results['page']['totalPages']-1):
            all_content.extend((search_calcs_results(requestID, i, size = 1000))['content'])

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(all_content)

        # Extract calculations from dataframe column (calculations). They are all isted here as a dictionary json object
        df_calculations = pd.json_normalize(df['calculations'])

        # Concatenate the calculations dataframe with the original dataframe and drop the now empty calculation column
        df = pd.concat([df, df_calculations], axis=1).drop('calculations', axis=1)

    else:

        print("No search conditions defined, check for tag name errors")

    EventDefinitions[eventDefinition]['results'] = df[['start', 'end', 'duration'] + [calc['name'] for calc in search_calculations]]
