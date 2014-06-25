'''
Created on Feb 24, 2014

@author: leal
'''
import unittest

from query.validator.queryval import QueryValidator
from config.config import configParser


class Test(unittest.TestCase):

    instrumentName = "IN5"
    instrumentNameOriginal = None; 
    
    validJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors": "12345,56789,12121"
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

    

    def testValidatorSuccess(self):
        content = self.validJson
        v = QueryValidator(content)
        message = v.validateQuery()
        self.assertEqual(message, None)

    def testValidatorInvalidJson(self):
        content = self.invalidJson
        v = QueryValidator(content)
        message = v.validateQuery()
        self.assertDictContainsSubset({'success' : 'False'}, message)
    


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testValidatorNexus']
    unittest.main()
