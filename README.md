This command line appplication is written in Python. This app allows CRUD operations against Salesforce bulk API: http://www.salesforce.com/us/developer/docs/api_asynch/index.htm

## How-to

In your terminal, go to the bulkly folder
> cd bulkly

Then run the following
> python bulkly.py --user [User Name] --pw [Password] --token [Token]

## Code structure

The app has following structure:

bulkly.py             the CLI app
libs/requests         python requests library
libs/sf_bulk.py       python wrapper for Salesforce bulk API

The file _bulkly.py_ is the CLI app which renders menu, processes user choices and calls Salesforce bulk api. The _requests library_ does http requests to Salesforce API endpoints. The _sf_bulk library_ is a simple wrapper for Salesforce bulk API.