'''
Created on Mar 13, 2014

@author: leal
'''
import unittest
import simplejson
from result.handler import ResultHandler

class Test(unittest.TestCase):

    def testResult(self):
        queryId = "257928e9-73a3-4422-bf20-2d0f80bf2a12"
        r = ResultHandler(queryId)
        res = r.getQuery()
        # convert string to dic
        res = simplejson.loads(res)
        self.assertEqual(res["status"], "done")
        self.assertEqual(res["start_local_time"], "Fri Apr  4 15:59:25 2014")
        self.assertEqual(res["instrument_name"], "D20")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testResult']
    unittest.main()