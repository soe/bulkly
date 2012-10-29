import sys
if('./libs' not in sys.path): sys.path.append('./libs')

import getopt
import getpass

import sf_bulk

BULK = sf_bulk.Bulk()

# Choice 1
def _create_job():
    jobObject = raw_input('Enter job object (i.e: Contact): ')
    jobType = raw_input('Enter job type (CSV, XML, ZIP_CSV, ZIP_XML): ')
    
    BULK.create_job(jobObject, jobType)

# Choice 2    
def _get_job():
    jobId = raw_input('Enter job ID to get: ')
    
    BULK.get_job(jobId)

# Choice 3    
def _close_job():
    jobId = raw_input('Enter job ID to close: ')
    
    BULK.close_job(jobId)

# Choice 4
def _abort_job():
    jobId = raw_input('Enter job ID to abort: ')

    BULK.abort_job(jobId)

# Choice 5  
def _add_batch():
    jobId = raw_input('Enter job ID for batch: ')
    fileName = raw_input('Enter batch file path: ')
    fileType = raw_input('Enter batch file type (CSV, XML, ZIP_CSV, ZIP_XML): ')
    
    BULK.add_batch(jobId, fileName, fileType)
    
# Choice 6
def _get_batches():
    jobId = raw_input('Enter job ID of the batches: ')
    
    BULK.get_batch(jobId)

# Choice 7    
def _get_batch():
    jobId = raw_input('Enter job ID of the batch: ')
    batchId = raw_input('Enter the batch ID: ')
    
    BULK.get_batch(jobId, batchId)
    
# Choice 8
def _get_batch_request():
    jobId = raw_input('Enter job ID of the batch: ')
    batchId = raw_input('Enter the batch ID: ')
    
    BULK.get_batch_result(jobId, batchId)

# Choice 8
def _get_batch_result():
    jobId = raw_input('Enter job I    D of the batch: ')
    batchId = raw_input('Enter the     batch ID: ')

    BULK.get_batch_result(jobId, batchId)
                        
def print_menu():
    print ('\nSalesforce Bulk API CLI\n'
        '1) Create Job\n'
        '2) Get Job\n'
        '3) Close Job\n'
        '4) Abort Job\n'
        '5) Add Batch\n'
        '6) Get Batches\n'
        '7) Get Batch\n'
        '8) Get Batch Request\n'
        '9) Get Batch Result\n'
        '0) Exit.\n'
    )
    
def get_menu_choice(max):
  while True:
    input = raw_input('> ')

    try:
      num = int(input)
    except ValueError:
      print 'Invalid choice. Please choose a value between 0 and', max
      continue

    if num > max or num < 0:
      print 'Invalid choice. Please choose a value between 10and', max
    else:
      return num
      
def show_menu():
    try:
        while True:
            print_menu()
            choice = get_menu_choice(9)

            if choice == 1:
                _create_job()
            elif choice == 2:
                _get_job()
            elif choice == 0:
                print '\nGoodbye.'
                return
    except KeyboardInterrupt:
        print '\nGoodbye.'
        return

def main():
    # Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
    except getopt.error, msg:
        print 'python bulkly.py --user [username] --pw [password] '
        sys.exit(2)

    user = ''
    pw = ''
    key = ''

    # Process options
    for option, arg in opts:
        if option == '--user':
            user = arg
        elif option == '--pw':
            pw = arg

    while not user:
        user = raw_input('Please enter your username: ')

    while not pw:
        pw = getpass.getpass('Please enter your password with security code: ')
        if not pw:
            print 'Password cannot be blank.'

    login = BULK.login(user, pw)
    
    if login:
        print 'Login successful.'
        show_menu()
        
    else:
        print 'Invalid user credentials given.'
        return


if __name__ == '__main__':
    main()
