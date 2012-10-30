'''
    Salesforce BULK API wrapper
    http://www.salesforce.com/us/developer/docs/api_asynch/index.htm
'''

import inspect

import requests
from xml.dom.minidom import parseString

LOGIN_ENDPOINT = 'https://login.salesforce.com/services/Soap/u/26.0'
BULK_ENDPOINT = 'https://%(instance)s.salesforce.com/services/async/26.0/job'

class Bulk(object):

    def __init__(self):
        self.username = ''
        self.password = ''
        self.instance = ''
        self.sessionId = ''


    def login(self, username, password):
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

        self.username = username
        self.password = password

        data = xml_template % {'username': self.username, 'password': self.password}
        url = LOGIN_ENDPOINT

        r = requests.post(url, headers = headers, data = data)

        if r.status_code == 200:

            xmltree = parseString(r.text)

            sessionId = xmltree.getElementsByTagName('sessionId')[0].childNodes[0].wholeText
            serverUrl = xmltree.getElementsByTagName('serverUrl')[0].childNodes[0].wholeText

            print 'login successful'
            print 'sessionId: %s' % sessionId
            print 'serverUrl: %s' % serverUrl

            self.sessionId = sessionId
            self.instance = serverUrl.split('.salesforce.com')[0].split('https://')[1]

            return (sessionId, serverUrl)

        else:
            self.show_failed_message(inspect.stack()[0][3], r)

            return None

    def create_job(self, jobOperation, jobObject, jobType):
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
            'X-SFDC-Session': self.sessionId
        }

        data = xml_template % {'operation': jobOperation, 'object': jobObject, 'contentType': jobType}
        url = BULK_ENDPOINT % {'instance': self.instance}

        r = requests.post(url, headers = headers, data = data)

        if r.status_code == 201:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    def get_job(self, jobId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_get_details.htm'''

        headers = {
            'X-SFDC-Session': self.sessionId
        }

        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId

        data = {}
        r = requests.get(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

    def close_job(self, jobId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_close.htm'''

        xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
        <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
          <state>Closed</state>
        </jobInfo>'''

        headers = {
            'Content-Type': 'application/xml; charset=UTF-8',
            'X-SFDC-Session': self.sessionId
        }

        data = xml_template
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId

        r = requests.post(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

    def abort_job(self, jobId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_jobs_abort.htm'''

        xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
        <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
          <state>Aborted</state>
        </jobInfo>'''

        headers = {
            'Content-Type': 'application/xml; charset=UTF-8',
            'X-SFDC-Session': self.sessionId
        }

        data = xml_template
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId

        r = requests.post(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

    def add_batch(self, jobId, fileName, fileType):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_create.htm'''

        fileTypes = {'CSV': 'text/csv', 'XML': 'text/xml', 'ZIP_CSV': 'zip/csv', 'ZIP_XML': 'zip/xml'}

        headers = {
            'Content-Type': fileTypes[fileType] +'; charset=UTF-8',
            'X-SFDC-Session': self.sessionId
        }

        data = {}
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId + '/batch'
        
        f = open(fileName, 'rb')

        r = requests.post(url, headers = headers, data = f.read())
        
        f.close()
        
        if r.status_code == 201:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    def get_batches(self, jobId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_info_all.htm'''

        headers = {
            'X-SFDC-Session': self.sessionId
        }

        data = {}
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId + '/batch'

        r = requests.get(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    def get_batch(self, jobId, batchId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_info.htm'''

        headers = {
            'X-SFDC-Session': self.sessionId
        }

        data = {}
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId + '/batch/' + batchId

        r = requests.get(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    def get_batch_request(self, jobId, batchId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_request.htm'''

        headers = {
            'X-SFDC-Session': self.sessionId
        }

        data = {}
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId + '/batch/' + batchId + '/request'

        r = requests.get(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    def get_batch_result(self, jobId, batchId):
        '''http://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_batches_get_results.htm'''

        headers = {
            'X-SFDC-Session': self.sessionId
        }

        data = {}
        url = BULK_ENDPOINT % {'instance': self.instance} + '/'+ jobId + '/batch/' + batchId + '/result'

        r = requests.get(url, headers = headers, data = data)

        if r.status_code == 200:
            self.show_successful_message(inspect.stack()[0][3], r)
        else:
            self.show_failed_message(inspect.stack()[0][3], r)

        return r

    # show success message
    def show_successful_message(self, functionName, r):
        print functionName + ' - successful'
        print r.text
            
    # show fail message    
    def show_failed_message(self, functionName, r):
        print functionName + ' - failed'
        print 'status_code: %s, reason: %s' % (r.status_code, r.reason)
        print r.text