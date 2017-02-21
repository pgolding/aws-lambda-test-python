from __future__ import print_function


import unittest
import awslambda
import simulate
import json

# Initialize the event test object to pass into Lambda function
evt = awslambda.LambdaEvent()
evt.load_event()


class TestLambdaMethods(unittest.TestCase):
    
    # Make sure we can set up the test data
    def test_event_setup_ok(self):
        self.assertTrue('httpMethod' in evt.event)
        
    # Example test   
    def test_event_post(self):
        evt.set_field('httpMethod','POST')
        # do something that requires POST method
        self.assertTrue(False)
        
    # Example test
    def test_event_get(self):
        evt.set_field('httpMethod','GET')
        res = json.loads(simulate.test()['body'])
        # do something that requires GET method
        self.assertTrue(False)
        
if __name__ == '__main__':
    unittest.main()