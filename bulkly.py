import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import requests
import simplejson as json
import urllib

LOGIN_ENDPOINT = 'https://login.salesforce.com/services/Soap/u/26.0'
BULK_ENDPOINT = 'https://%(instance)s.salesforce.com/services/async/26.0/job'

def login(username, password):
    
    xml_template = '''<?xml version="1.0" encoding="utf-8" ?>
    <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
      <env:Body>
        <n1:login xmlns:n1="urn:partner.soap.sforce.com">
          <n1:username>%(username)s</n1:username>
          <n1:password>%(password)s</n1:password>
        </n1:login>
      </env:Body>
    </env:Envelope>'''
    
    data = { 'username': username, 'password': password }
    
    headers = {
        'SOAPAction': 'login', 
        'Content-Type': 'text/xml; charset=UTF-8', 
    }
    
    url = LOGIN_ENDPOINT
    
    r = requests.post(url, headers = headers, data = xml_template%data)
    
    print r.text
    
    return r
    
def create(instance, sessionId):
    
    xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
        <operation>%(operation)s</operation>
        <object>%(object)s</object>
        <contentType>%(contentType)s</contentType>
    </jobInfo>'''
    
    data = {'operation': 'insert', 'object': 'Contact', 'contentType': 'CSV'}
    
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8', 
        'Authorization': 'Bearer '+ sessionId
    }
    
    url = BULK_ENDPOINT%{'instance': instance}
    
    r = requests.post(url, headers = headers, data = xml_template%data)
    
    print r.text
    
    return r
    
def read():
    pass
    
def update():
    pass
    
def delete():
    pass
    
    