'''
Created on Feb 24, 2014

@author: leal
'''
import unittest

from query.handler import QueryHandler
from config.config import configParser

class Test(unittest.TestCase):

    instrumentName = "IN5"
    instrumentNameOriginal = None; 
    
    validJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors":"094460"
        }
    }"""
    
    invalidJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors": 12345,56789,12121
        }
    }"""

    def setUp(self):
        # For the tests to pass
        self.instrumentNameOriginal = configParser.get("General", "instrument_name")
        configParser.set("General", "instrument_name", self.instrumentName)
    
    def tearDown(self):
        configParser.set("General", "instrument_name", self.instrumentNameOriginal)

    
    def testHandlerValid(self):
        content = self.validJson
        qh = QueryHandler(content)
        message = qh.process()
        print message
        self.assertDictContainsSubset({'timeout' : 30}, message)

    def testHandlerInvalidJson(self):
        content = self.invalidJson
        qh = QueryHandler(content)
        message = qh.process()
        self.assertDictContainsSubset({'success' : 'False'}, message)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testValidatorNexus']
    unittest.main()