import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import requests
import simplejson as json

from xml.dom.minidom import parseString

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
    
    headers = {
        'SOAPAction': 'login', 
        'Content-Type': 'text/xml; charset=UTF-8', 
    }
    
    url = LOGIN_ENDPOINT
    
    data = xml_template % {'username': username, 'password': password}
    r = requests.post(url, headers = headers, data = data)
    
    if r.status_code == 200:
    
        xmltree = parseString(r.text)
    
        sessionId = xmltree.getElementsByTagName('sessionId')[0].childNodes[0].wholeText
        serverUrl = xmltree.getElementsByTagName('serverUrl')[0].childNodes[0].wholeText
        
        print 'login successful'
        print 'sessionId: %s' % sessionId
        print 'serverUrl: %s' % serverUrl
    
    else: 
        print 'login failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
    
    return r
    
def create_job(instance, sessionId):
    
    xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
        <operation>%(operation)s</operation>
        <object>%(object)s</object>
        <contentType>%(contentType)s</contentType>
    </jobInfo>'''
    
    headers = {
        'Content-Type': 'application/xml; charset=UTF-8', 
        'X-SFDC-Session': sessionId
    }
    
    data = xml_template % {'operation': 'insert', 'object': 'Contact', 'contentType': 'CSV'}
    url = BULK_ENDPOINT % {'instance': instance}
    
    r = requests.post(url, headers = headers, data = data)
    
    if r.status_code == 201:
        
        xmltree = parseString(r.text)
        
        job_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'create_job successful'
        print r.text
        
    else:
        print 'create_job failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)        
    
    return r

def add_batch(instance, sessionId, jobId, fileName):

    headers = {
        'Content-Type': 'text/csv; charset=UTF-8', 
        'X-SFDC-Session': sessionId
    }
    
    data = {'title': fileName}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch'
    
    r = requests.post(url, headers = headers, data = data, files = {'file': open(fileName)})

    if r.status_code == 201:
        
        xmltree = parseString(r.text)
        
        batch_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'add_batch successful'
        print r.text
        
    else:
        print 'add_batch failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)        
    
    return r
        
def close_job(instance, sessionId, jobId):
    
    xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
      <state>Closed</state>
    </jobInfo>'''
        
    headers = {
        'Content-Type': 'application/xml; charset=UTF-8', 
        'X-SFDC-Session': sessionId
    }
    
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId
    
    r = requests.post(url, headers = headers, data = xml_template)
    
    if r.status_code == 201:
        
        xmltree = parseString(r.text)
        
        job_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'close_job successful'
        print r.text
        
    else:
        print 'close_job failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)        

def check_batches(instance, sessionId, jobId):

    headers = {
        'X-SFDC-Session': sessionId
    }
    
    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch'
    
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:
        
        xmltree = parseString(r.text)
        
        batch_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'check_batch successful'
        print r.text
        
    else:
        print 'check_batches failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)        
    
    return r
        
def check_batch(instance, sessionId, jobId, batchId):

    headers = {
        'X-SFDC-Session': sessionId
    }
    
    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch/' + batchId
    
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:
        
        xmltree = parseString(r.text)
        
        batch_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'check_batch successful'
        print r.text
        
    else:
        print 'check_batch failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)        
    
    return r

def retrieve_batch(instance, sessionId, jobId, batchId):
    pass    