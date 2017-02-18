# AWS Lambda Test Harness (Python 2.7)

If you find yourself often creating Lambda Functions (LF) and editing code in-line, it might be easier to run your LF on your local machine. In priniciple, this is easy because, after all, it's just a block of Python code. The idea is to store your LF locally (typically ```lambda_function.py```) and then call it from a test program - ```test.py```

However, there are a few housekeeping issues to settle:

- Making sure you're on Python 2.7 (or whatever AWS LF supports)
- Reproducing any environment vars, like KMS-encrypted API keys
- Logging compatibility (with AWS logging root)
- Passing in the 'event' and 'context' objects 
- Using the correct AWS IAM role

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

### Logging

It is good practice to use the logging module rather than print. This allows you to control the level of logging (info, error, debug, etc.) and adds a timestamp. However, when running on AWS, you'll need to point your logger to the root log (so that AWS can push the logs to your log stream/log group). Whilst running locally, there will be no root and so you should set it to the current namespace of the app. This requires a conditional setup in your LF, like:

```python
# This test is for when using the local testing harness
if 'LAMBDA_TEST' in os.environ:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger()
```

This relies on setting the environment variable LAMBDA_TEST from the test harness. Of course, on the AWS servers this will not be set and so the logger will default to the root ```logging.getLogger()```

### Roles

Ideally, you should simulate your local LF using the same role as the LF deployed on AWS. To do this, make sure that you set up a role in your ```~/.aws/configure``` and make it point to the profile that you wish to use:

```
[profile <profile_name>]
role_arn = arn:aws:iam::123456789012:role/somerole
source_profile = development
```

In this case, I have set the role_arn (which you can get from [the IAM console](https://console.aws.amazon.com/iam)) and pointed it to an AWS credentials profile 'development' (set in ```~/.aws/credentials```). I just need to do two things now:

1. Make sure I set the AWS default profile to the one I want

>export AWS_DEFAULT_PROFILE=development

2. Make sure that the profile credentials have permission to invoke sts:AssumeRole on the role_arn by adding the following policy to the default profile (AWS IAM user) for these tests.

```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": "arn:aws:iam::123456789012:role/somerole"
  }]
}
```

You should check you're using the right IAM settings:

>aws configure

### Event Object

Finally, you need to call your lambda handler by passing in an event object that simulates the object that will get passed to your LF when it runs on AWS. You should add the event object JSON data to the file ```lambda-event.json``` and then it's ready to pass into your handler. However, you might be wondering how to get that data.

There are two ways. The best way, and is an implicit assumption in setting up this test, is to first deploy your LF on AWS and connect it to the trigger condition, such as an object creation in S3. Then run the condition and use a basic lamba handler to pass that data out to the logs.

```python
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
```

Then go to the logs for your LF and look for 'Received event:' to find the dump from the event object. Then cut and paste this into the ```lamda-event.json``` file. Then you're ready to go.

Alternatively, if you haven't yet set up the trigger, then you can use the various test templates already loaded into the AWS LF environment - select "Configure test event" from the Actions menu.

![screenshot 2017-02-18 15 20 48](https://cloud.githubusercontent.com/assets/28526/23097676/708e1bfa-f5ee-11e6-93ea-9e698b55f1f0.png)

All being well, you should be ready to go and test your LF

>python test.py

Happy testing :+1: