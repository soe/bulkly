import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import requests
import simplejson as json
import urllib

AUTH_ENDPOINT = 'https://login.salesforce.com/services/oauth2/token'

CLIENT_ID = '3MVG99qusVZJwhskz0FeVuqB0cuGHEyLIjaXu7IiufybfuF8HDUx0WMBGClbdUhWj86J44Sico.Y41E4UOheM'
CLIENT_SECRET = '2042840911220509737'

def login(username, password):
    
    payload = {
        'username': username,
        'password': password,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password'
    }
    
    headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    }
    
    r = requests.post(AUTH_ENDPOINT, data = urllib.urlencode(), headers = headers)
    
    print r.text
    
def create():
    pass
    
def read():
    pass
    
def update():
    pass
    
def delete():
    pass
    
    