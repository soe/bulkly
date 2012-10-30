import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import getopt
import getpass

# import salesforce bulk api wrapper
import sf_bulk

# initiate salesforce bulk api wrapper
BULK = sf_bulk.Bulk()

# mapping for menu names and functions
CHOICES0 = ['Create Job', 'Get Job', 'Close Job', 'Abort Job', 'Add Batch', 'Get Batches', 'Get Batch', 'Get Batch Request', 'Get Batch Result']
CHOICES1 = ['create_job', 'get_job', 'close_job', 'abort_job', 'add_batch', 'get_batches', 'get_batch', 'get_batch_request', 'get_batch_result']

def _create_job():
    jobObject = raw_input('Enter job object (i.e: Contact): ')
    jobType = raw_input('Enter job type (CSV, XML): ')
    
    BULK.create_job(jobObject, jobType)

def _get_job():
    jobId = raw_input('Enter job ID to get: ')
    
    BULK.get_job(jobId)

def _close_job():
    jobId = raw_input('Enter job ID to close: ')
    
    BULK.close_job(jobId)

def _abort_job():
    jobId = raw_input('Enter job ID to abort: ')

    BULK.abort_job(jobId)

def _add_batch():
    jobId = raw_input('Enter job ID for batch: ')
    fileName = raw_input('Enter batch file path: ')
    fileType = raw_input('Enter batch file type (CSV, XML): ')
    
    BULK.add_batch(jobId, fileName, fileType)
    
def _get_batches():
    jobId = raw_input('Enter job ID of the batches: ')
    
    BULK.get_batch(jobId)

def _get_batch():
    jobId = raw_input('Enter job ID of the batch: ')
    batchId = raw_input('Enter the batch ID: ')
    
    BULK.get_batch(jobId, batchId)
    
def _get_batch_request():
    jobId = raw_input('Enter job ID of the batch: ')
    batchId = raw_input('Enter the batch ID: ')
    
    BULK.get_batch_result(jobId, batchId)

def _get_batch_result():
    jobId = raw_input('Enter job ID of the batch: ')
    batchId = raw_input('Enter the batch ID: ')

    BULK.get_batch_result(jobId, batchId)
                           
def print_menu():
    print('\nSalesforce Bulk API CLI')
    
    for i, j in enumerate(CHOICES0):
        print(str(i + 1) + ') ' + j)
    
    print('0) Exit.\n')
    
def get_menu_choice(max):
  while True:
    choice = raw_input('> ')

    try:
      choice = int(choice)
    except ValueError:
      print 'Invalid choice. Please choose a value between 0 and', max
      continue

    if choice > max or choice < 0:
      print 'Invalid choice. Please choose a value between 0 and', max
    else:
      return choice
      
def show_menu():
    try:
        while True:
            print_menu()
            choice = get_menu_choice(len(CHOICES0))
            
            if choice == 0:
                print '\nGoodbye.'
                return
            else:
                globals()['_' + CHOICES1[choice - 1]]()
                
    except KeyboardInterrupt:
        print '\nGoodbye.'
        return

def main():

    user = ''
    pw = ''
    token = ''

    # Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'token='])
    except getopt.error, msg:
        print 'python bulkly.py --user [username] --pw [password] --token [token]'
        sys.exit(2)

    # Process options
    for option, arg in opts:
        if option == '--user':
            user = arg
        elif option == '--pw':
            pw = arg
        elif option == '--token':
            token = arg
    
    # prompt for user to enter if not defined yet...        
    while not user:
        user = raw_input('Please enter your username: ')
        if not user:
            print 'Username cannot be blank.'

    # prompt for user to enter if not defined yet...  
    while not pw:
        pw = getpass.getpass('Please enter your password: ')
        if not pw:
            print 'Password cannot be blank.'

    # prompt for user to enter if not defined yet...  
    while not token:
        token = getpass.getpass('Please enter your security token: ')
        if not token:
            print 'Security token cannot be blank.'
    
    # do login                                    
    login = BULK.login(str(user), str(pw) + str(token))
    
    if login:
        print 'Login successful.'
        show_menu()
        
    else:
        print 'Invalid user credentials given.'
        return
        
        
if __name__ == '__main__':
    main()
