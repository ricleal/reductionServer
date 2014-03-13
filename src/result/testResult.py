'''
Created on Mar 13, 2014

@author: leal
'''
import unittest

from result.handler import HandlerResult

class Test(unittest.TestCase):


    def testResult(self):
        queryId = "76d5c930-1737-4dbc-80e0-dbc34339a0e7"
        r = HandlerResult(queryId)
        res = r.getQuery()
        print res
        self.assertIn('status',res)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testResult']
    unittest.main()