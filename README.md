# AWS Lambda Test Harness (Python 2.7)

If you find yourself often creating Lambda Functions (LF) and editing code in-line, it might be easier to run your LF on your local machine. In priniciple, this is easy because, after all, it's just a block of Python code.

However, there are a few housekeeping issues to settle:

- Making sure you're on Python 2.7 (or whatever AWS LF supports)
- Reproducing any environment vars, like KMS-encrypted API keys
- Logging compatibility (with AWS logging root)
- Passing in the 'event' and 'context' objects 

### Python Check 

Currently AWS only supports Python 2.7 for AWS LF. This means you need to make sure that you are testing locally with Python 2.7. If you are using a virtual env setup like Anaconda, then you should create a conda env, something like:

>conda create -n aws python=3.4

And then activate it:

>active source aws

Nonetheless, the script contains a quick check for Python 2.7

```python
LAMBDA_RUNTIME = '2.7'
if LAMBDA_RUNTIME not in sys.version.split(' ')[0]:
    logger.error('Wrong version of Python')
    exit()
```