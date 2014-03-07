'''
Created on Feb 24, 2014

@author: leal
'''
import unittest

from query.validator.queryval import QueryValidator

class Test(unittest.TestCase):

    validJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors":[
                12345,
                56789,
                12121
            ]
        }
    }"""
    
    invalidJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors": 12345,56789,12121
        }
    }"""
    

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
    #import sys;sys.argv = ['', 'Test.testValidatorNexus']
    unittest.main()