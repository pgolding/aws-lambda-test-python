'''
This file is a template for locally testing Lambda functions in Python 2.7
It requires the existence of a local file 'lambda-event.json' that contains the simulated 'event' object.
This is similar to the test data that gets used to test Lambda functions in the AWS environment.
NOTE: no attempt is made here to simlulate the 'context' object


'''
import json
import os
import sys
import logging
# Set environment var to let Lambda function know we are testing
# DO THIS FIRST
os.environ['LAMBDA_TEST'] = 'True'   


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Loading Lambda Test Function')
# Only import lambda function after setting LAMBDA_TEST env var
import lambda_function

# Don't forget to switch to Python 2.7 for testing Lambda functions
LAMBDA_RUNTIME = '2.7'
if LAMBDA_RUNTIME not in sys.version.split(' ')[0]:
    logger.error('Wrong version of Python')
    exit()

# Don't forget to set any keys used by Lambda function on AWS (e.g. KMS keys etc.)
APIKEY = 'AQECAHi+cZAiuTwzWIe727iJYVmf0wb0pvlfHqoDq2w7g2SJIQAAAIcwgYQGCSqGSIb3DQEHBqB3MHUCAQAwcAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxQl4I3IN+ILjWBsXMCARCAQ3wJ1oQyWgGKr/TgzKZBk4CnagtF8ebxU5l+cKIeBxhwgbvQfoQDM50+Ap2EIueTEUrPRZAKkWD96BkyKKc6/worlH4='
os.environ['APIKEY'] = APIKEY

# Make sure that the trigger event data exists to pass into the handler
if os.path.exists('lambda-event.json'):
    try:
        lambda_event = json.loads(open('lambda-event.json').read())
        res = lambda_function.lambda_handler(lambda_event, None)
        logger.info('Lambda function returned:\n{}'.format(res))
    except Exception as e:
        logger.error(e)
else:
    logger.error('No Lambda event json file present to pass into lambda_handler. Please check files.')
    

# Finally clean-up:
if 'APIKEY' in os.environ: os.environ.pop('APIKEY')
if 'LAMBDA_TEST' in os.environ: os.environ.pop('LAMBDA_TEST')
