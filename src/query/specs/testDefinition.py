'''
Created on Feb 25, 2014

@author: leal
'''
import unittest

from query.specs.definition import QuerySpecs

class Test(unittest.TestCase):


    def testQuery(self):
        q = QuerySpecs()
        
        self.assertTrue(q.doesFunctionExist("theta_vs_counts"))
        
        self.assertFalse(q.doesFunctionExist("theta_vs_counts1"))
        
        self.assertEqual(q.getExecutableFullPath("theta_vs_counts"), 
                         "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py")
        self.assertEqual(q.getExecutableTimeout("theta_vs_counts"), 30)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testQuery']
    unittest.main()
