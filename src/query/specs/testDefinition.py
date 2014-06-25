'''
Created on Feb 25, 2014

@author: leal
'''
import unittest

from query.specs.definition import QuerySpecs
from config.config import configParser

class Test(unittest.TestCase):
    
    instrumentName = "IN5"
    instrumentNameOriginal = None; 
    
    def setUp(self):
        # For the tests to pass
        self.instrumentNameOriginal = configParser.get("General", "instrument_name")
        configParser.set("General", "instrument_name", self.instrumentName)
    
    def tearDown(self):
        configParser.set("General", "instrument_name", self.instrumentNameOriginal)

    def testQuery(self):
        
        q = QuerySpecs()
        
        self.assertTrue(q.doesFunctionExist("theta_vs_counts"))
        
        self.assertFalse(q.doesFunctionExist("theta_vs_counts1"))
        
        self.assertEqual(q.getExecutableFullPath("theta_vs_counts"),
                         "/home/leal/git/reductionServer/src/query/scripts/ILL_IN5_theta_vs_counts.py")
        self.assertEqual(q.getExecutableTimeout("theta_vs_counts"), 30)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testQuery']
    unittest.main()
