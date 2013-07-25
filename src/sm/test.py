'''
Created on Jul 25, 2013

@author: leal
'''
import unittest
import handler

class Test(unittest.TestCase):

    def testHandler(self):
        h = handler.Handler()
        sm = h.sm() 
        
        sm.enterStartState()
        
        #TODO
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()