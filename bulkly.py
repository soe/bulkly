import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import requests
import simplejson as json

from xml.dom.minidom import parseString

LOGIN_ENDPOINT = 'https://login.salesforce.com/services/Soap/u/26.0'
BULK_ENDPOINT = 'https://%(instance)s.salesforce.com/services/async/26.0/job'

def login(username, password):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_quickstart_login.htm'''
    
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
        print 'body: %s' % r.text 
    
    return r
    
def create_job(instance, sessionId, jobObject, jobType):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_create.htm'''
    
    jobTypes = {'CSV': 'text/csv', 'XML': 'text/xml', 'ZIP_CSV': 'zip/csv', 'ZIP_XML': 'zip/xml'}
    
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
    
    data = xml_template % {'operation': 'insert', 'object': jobObject, 'contentType': jobType}
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
        print 'body: %s' % r.text        
    
    return r

def get_job(instance, sessionId, jobId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_get_details.htm'''

    headers = {
        'X-SFDC-Session': sessionId
    }

    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId

    data = {}
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:

        xmltree = parseString(r.text)

        job_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText

        print 'get_job successful'
        print r.text

    else:
        print 'get_job failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text 
            
def close_job(instance, sessionId, jobId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_close.htm'''

    xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
      <state>Closed</state>
    </jobInfo>'''

    headers = {
        'Content-Type': 'application/xml; charset=UTF-8', 
        'X-SFDC-Session': sessionId
    }

    data = xml_template
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId

    r = requests.post(url, headers = headers, data = data)

    if r.status_code == 200:

        xmltree = parseString(r.text)

        job_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText

        print 'close_job successful'
        print r.text

    else:
        print 'close_job failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text 

def abort_job(instance, sessionId, jobId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_abort.htm'''

    xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
      <state>Aborted</state>
    </jobInfo>'''

    headers = {
        'Content-Type': 'application/xml; charset=UTF-8', 
        'X-SFDC-Session': sessionId
    }

    data = xml_template
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId

    r = requests.post(url, headers = headers, data = data)

    if r.status_code == 200:

        xmltree = parseString(r.text)

        job_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText

        print 'abort_job successful'
        print r.text

    else:
        print 'abort_job failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text 
            
def add_batch(instance, sessionId, jobId, fileName, fileType):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_create.htm'''

    fileTypes = {'CSV': 'text/csv', 'XML': 'text/xml', 'ZIP_CSV': 'zip/csv', 'ZIP_XML': 'zip/xml'}
    
    headers = {
        'Content-Type': fileTypes[fileType] +'; charset=UTF-8', 
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
        print 'body: %s' % r.text        
    
    return r
        
def get_batches(instance, sessionId, jobId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_info_all.htm'''

    headers = {
        'X-SFDC-Session': sessionId
    }
    
    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch'
    
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:
        
        xmltree = parseString(r.text)
        
        batch_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'get_batch successful'
        print r.text
        
    else:
        print 'get_batches failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text         
    
    return r
        
def get_batch(instance, sessionId, jobId, batchId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_info.htm'''

    headers = {
        'X-SFDC-Session': sessionId
    }
    
    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch/' + batchId
    
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:
        
        xmltree = parseString(r.text)
        
        batch_id = xmltree.getElementsByTagName('id')[0].childNodes[0].wholeText
        
        print 'get_batch successful'
        print r.text
        
    else:
        print 'get_batch failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text         
    
    return r

def get_batch_request(instance, sessionId, jobId, batchId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_request.htm'''

    headers = {
        'X-SFDC-Session': sessionId
    }

    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch/' + batchId + '/request'

    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:

        print 'get_batch_request successful'
        print r.text

    else:
        print 'get_batch_request failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text      

    return r
        
def get_batch_result(instance, sessionId, jobId, batchId):
    '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_results.htm'''

    headers = {
        'X-SFDC-Session': sessionId
    }
    
    data = {}
    url = BULK_ENDPOINT % {'instance': instance} + '/'+ jobId + '/batch/' + batchId + '/result'
    
    r = requests.get(url, headers = headers, data = data)

    if r.status_code == 200:
        
        print 'get_batch_result successful'
        print r.text
        
    else:
        print 'get_batch_result failed' 
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print 'body: %s' % r.text       
    
    return r    