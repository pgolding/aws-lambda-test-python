from __future__ import print_function

import json
import urllib
import boto3
import os
import logging
from base64 import b64decode

# This test is for when using the local testing harness
if os.environ['LAMBDA_TEST'] == 'True':
    print('LAMBDA_TEST: True')
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger()

logger.setLevel(logging.INFO)
logger.info('Loading Lambda Function')

ENCRYPTED = os.environ['APIKEY']
# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext']



s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        logger.info("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
    except Exception as e:
        logger.error(e)
        logger.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
