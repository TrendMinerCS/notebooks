import requests
import json
import itertools
import pandas as pd

url = 'https://dsitl-demo.trendminer.cloud'

def get_plot_data(name, start, end, intervals):
    """Get time series plot data for a given timeframe. Can return trendminer index data or datasource (raw) data

        Parameters
        ----------
        start : str
            Data interval start time as a string. Format: 2022-01-01T00:00:00.000Z
        end : str
            Data interval start time as a string. Format: 2022-01-02T00:00:00.000Z
        intervals : int
            Number of intervals in which the given period should be split. One interval can contain 0 to 4 points (first, last, min, max).
            When the interval length (duration/intervals) is less than the index resolution, the request is passed to the datasource which
            can return plot-optimized or raw data depending on the number of intervals requested, and the type of datasource.
            
        Returns
        -------
        pandas.Series
            tag values with timestamp as index
        """    
    
    token = "{TM_TOKEN.password}"

    headers = {'Authorization': f'Bearer {token}'}
    
    params = {
        'tagName': name
    }
    
    r = requests.get(f'{url}/hps/api/tags/details', params=params, headers=headers)
    
    interpolation_type = r.json()['interpolationType']
    numeric = r.json()['type'] in ['ANALOG', 'DISCRETE']
    states = {s['Code']: s['Name'] for s in r.json().get('States', [])}
    
    params = {
        'tagNames[]': name,
        'startDate': start,
        'endDate': end,
        'numberOfIntervals': int(intervals/2), # real number is twice the requested number
        'interpolationTypes[]': interpolation_type,
        'shifts[]': 0
    }
    
    r = requests.get(f'{url}/compute/focusChart', params=params, headers=headers)
    
    
    data = pd.DataFrame.from_records((r.json()[0]['values']))
    
    if data.empty:
        if numeric:
            dtype = 'float'
        else:
            dtype = 'string'
        return pd.Series(index=pd.DatetimeIndex([], name='ts'), dtype=dtype, name=name)
        
    data['ts'] = pd.to_datetime(data['ts'])
    data.set_index('ts', inplace=True)
    data = data['value']
    data.name = name
    
    data = data.astype(float)
    
    if not numeric:
        data = data.map(states)
        
    return data
 

plot_data = get_plot_data(name='BA:LEVEL.1', start='2022-01-01T00:00:00.000Z', end='2022-01-31T00:00:00.000Z', intervals=300)
