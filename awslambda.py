from __future__ import print_function


import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAMBDA_EVENT_TEMPLATE = 'lambda-event.json'
# The event data read from template

class LambdaEvent():
    def __init__(self):
        self.event = None
    
    
    def load_event(self):
        if os.path.exists(LAMBDA_EVENT_TEMPLATE):
            try:
                logger.info('Reading lambda-event-json')
                init_event_data = json.loads(open('lambda-event.json').read())
            except Exception as e:
                logger.error(e)
            finally:
                self.event = init_event_data

    def set_field(self,key,value):
        if self.event:
            if key in self.event:
                self.event[key] = value
    


