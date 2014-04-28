'''
Created on Feb 24, 2014

@author: leal
'''
import unittest

from query.handler import QueryHandler


class Test(unittest.TestCase):

    validJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors":[94460]
        }
    }"""
    
    invalidJson = """{
        "method":"theta_vs_counts",
        "params":{
            "numors": 12345,56789,12121
        }
    }"""
    

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