This command line appplication is written in Python. This app allows CRUD operations against Salesforce bulk API: http://www.salesforce.com/us/developer/docs/api_asynch/index.htm

## Bonus features

* Standalone app
  * The app does not require additional libraries
* Code seperation
 * bulkly.py - the CLI wrapper is sepearted from sf_bulk.py - the Salesforce bulk API wrapper
* Multi-Python
  * compatible with Python v 2.6, 2.7, 3.2, and 3.3
* Include easily in other Python apps
  * sf_bulk.py can be easily included in other Python apps. Refer to comments in the file.

## How-to

In your terminal, go to the bulkly folder
> cd bulkly

Then run the following
> python bulkly.py --user [User Name] --pw [Password] --token [Token] --sandbox [sandbox]

Example
> python bulkly.py --user soe@cs.jsp2js.dev --pw FORCE2012 --token GGrFnoIJutesEweBNPxyCihx2

## Menu choices

_Choice 1 - Create Job_
> prompt: jobOperation, jobObject, jobType

_Choice 2 - Get Job_
> prompt: jobId

_Choice 3 - Close Job_
> prompt: jobId

_Choice 4 - Abort Job_
> prompt: jobId

_Choice 5 - Add Batch_
> prompt: jobId, fileName, fileType

_Choice 6 - Get Batches_
> prompt: jobId

_Choice 7 - Get Batch_
> prompt: jobId, batchId

_Choice 8 - Get Batch Request_
> prompt: jobId, batchId

_Choice 9 - Get Batch Request_
> prompt: jobId, batchId

## Code structure

The app has following structure:

bulkly.py             the CLI app
libs/requests         python requests library
libs/sf_bulk.py       python wrapper for Salesforce bulk API

The file _bulkly.py_ is the CLI app which renders menu, processes user choices and calls Salesforce bulk api. The _requests library_ does http requests to Salesforce API endpoints. The _sf_bulk library_ is a simple wrapper for Salesforce bulk API.