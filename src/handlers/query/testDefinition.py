'''
Created on Feb 25, 2014

@author: leal
'''
import unittest

from handlers.query.definition import Query

class Test(unittest.TestCase):


    def testQuery(self):
        q = Query()
        
        self.assertTrue(q.doesLocalFunctionExist("theta_vs_counts"))
        self.assertTrue(q.doesRemoteFunctionExist("theta_vs_counts"))
        self.assertFalse(q.doesLocalFunctionExist("theta_vs_counts1"))
        self.assertFalse(q.doesRemoteFunctionExist("theta_vs_counts1"))
        self.assertEqual(q.getExecutableFullPath("theta_vs_counts"), 
                         "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh")
        self.assertEqual(q.getExecutableTimeout("theta_vs_counts"), 30)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testQuery']
    unittest.main()
