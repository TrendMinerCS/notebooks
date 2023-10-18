def get_tag_details(tagname):
    
    params = {'tagName': tagname}
    
    r = requests.get(f'{serverUrl}/hps/api/tags/details', params=params, headers=auth_header)
    
    return r.json()
