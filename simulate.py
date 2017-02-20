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
import io
import awslambda
from boto3 import client as boto3_client
from base64 import b64encode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FUNCTION_NAME = 'napkin-glyph-s3-svg-trigger'
FUNCTION_LIBS = ['requests']

# Initialize the event data object
evt = awslambda.LambdaEvent()
evt.load_event()

def test():
    # Set LAMBDA_TEST to let Lambda function know we are testing
    # Set any vars before we load the Lambda function
    os.environ['LAMBDA_TEST'] = 'True'   
    # Don't forget to set any keys used by Lambda function on AWS (e.g. KMS keys etc.)
    APIKEY = 'AQECAHi+cZAiuTwzWIe727iJYVmf0wb0pvlfHqoDq2w7g2SJIQAAAIcwgYQGCSqGSIb3DQEHBqB3MHUCAQAwcAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxQl4I3IN+ILjWBsXMCARCAQ3wJ1oQyWgGKr/TgzKZBk4CnagtF8ebxU5l+cKIeBxhwgbvQfoQDM50+Ap2EIueTEUrPRZAKkWD96BkyKKc6/worlH4='
    os.environ['APIKEY'] = APIKEY


    logger.info('Loading Lambda Test Function')
    # Only import lambda function after setting LAMBDA_TEST env var
    import lambda_function

    # Don't forget to switch to Python 2.7 for testing Lambda functions
    LAMBDA_RUNTIME = '2.7'
    if LAMBDA_RUNTIME not in sys.version.split(' ')[0]:
        logger.error('Wrong version of Python')
        exit()

        # Make sure that the trigger event data exists to pass into the handler
    res = None
    if evt.event:
        try:
            res = lambda_function.lambda_handler(evt.event, None)
            logger.info('Lambda function returned:\n{}'.format(res))
        except Exception as e:
            logger.error(e)
    else:
        logger.error('No Lambda event json file present to pass into lambda_handler. Please check files.')
    # Finally clean-up:
    if 'APIKEY' in os.environ: os.environ.pop('APIKEY')
    if 'LAMBDA_TEST' in os.environ: os.environ.pop('LAMBDA_TEST')
    return res


def zip_path (path_to_be_zipped, target_zip_archive):
    if os.path.isdir(path_to_be_zipped):
        for dirpath,dirs,files in os.walk(path_to_be_zipped):
            for f in files:
                fn = os.path.join(dirpath,f)
                target_zip_archive.write(fn)
    else:
        target_zip_archive.write(path_to_be_zipped)


def upload(lambda_function='lambda_function.py', dependencies=[]):
    lambda_client = boto3_client('lambda')
    import zipfile
    zf = FUNCTION_NAME + ".zip"
    logger.info('Zipping lambda project files')
    with zipfile.ZipFile(zf, 'w') as code_archive:
        code_archive.write(lambda_function)
        for filename in dependencies:
            zip_path(filename, code_archive)
    try:
        logger.info('Uploading code')
        with open(zf, 'rb') as code_archive:
            data = code_archive.read()
            lambda_client.update_function_code(FunctionName=FUNCTION_NAME, ZipFile=data)
    except Exception as e:
        logger.error(e)


def main():
    arg = sys.argv[1]
    if arg == 'test':
        print('Testing lambda function')
        test()
    elif arg == 'upload':
        upload('lambda_function.py', FUNCTION_LIBS)
    else:
        print("Valid arguments are 'previews' or 'upload'. Please try again.")

if __name__ == "__main__":
    main()