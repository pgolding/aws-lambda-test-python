# AWS Lambda Test Harness (Python 2.7)

If you find yourself often creating Lambda Functions (LF) and editing code in-line, it might be easier to run your LF on your local machine. In priniciple, this is easy because, after all, it's just a block of Python code. The idea is to store your LF locally (typically lambda_function.py) and then call it from a test program - https://github.com/pgolding/aws-lambda-test-python/blob/master/test.py

However, there are a few housekeeping issues to settle:

- Making sure you're on Python 2.7 (or whatever AWS LF supports)
- Reproducing any environment vars, like KMS-encrypted API keys
- Logging compatibility (with AWS logging root)
- Passing in the 'event' and 'context' objects 

### Python Environment 

Currently AWS only supports Python 2.7 for AWS LF. This means you need to make sure that you are testing locally with Python 2.7. If you are using a virtual env setup like Anaconda, then you should create a conda env specifically for AWS, something like:

>conda create -n aws python=3.4

And then activate it:

>source activate aws

Nonetheless, the script contains a quick check for Python 2.7

```python
LAMBDA_RUNTIME = '2.7'
if LAMBDA_RUNTIME not in sys.version.split(' ')[0]:
    logger.error('Wrong version of Python')
    exit()
```

And then don't forget to install the [Boto3 library](https://boto3.readthedocs.io/en/latest/)

>conda install boto3

### Environment Variables

You can set environ vars for your LF when running on AWS. A typical, and highly recommended, use case is to store any data that is sensitive, like api keys. These should be encrypted using AWS KMS. You'll then require some code to retreive them, something like:

```python
ENCRYPTED = os.environ['APIKEY']
# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext']
```

Such vars need to be set locally for your test. This should be done via a standard OS call from Python:

```python
# Don't forget to set any keys used by Lambda function on AWS (e.g. KMS keys etc.)
APIKEY = 'AQECAHi+cZAiuTwzWIe727iJYVmf0wb0pvlfHqoD...rlH4='
os.environ['APIKEY'] = APIKEY
```