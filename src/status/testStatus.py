'''
Created on Mar 13, 2014

@author: leal
'''
import unittest

from status.handler import StatusHandler

class Test(unittest.TestCase):

    def testResult(self):
        
        r = StatusHandler()
        res = r.getQueries()
        print res
        self.assertGreater(len(res),0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testResult']
    unittest.main()