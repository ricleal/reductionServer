'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import os

from pythonlauncher import PythonScriptLauncher

class Test(unittest.TestCase):

    tmpfile = '/tmp/test12324.py'

    def setUp(self):
        f = open(self.tmpfile, 'w')
        f.write("import time\n")
        f.write("print 'Starting...'\n")
        f.write("a = 1\n")
        f.write("time.sleep(0.5)\n")
        f.write("b = 2\n")
        f.write("if locals().has_key('c'):\n")
        f.write("\tc=True\n")
        f.write("print 'Finishing...'\n")


    def tearDown(self):
        os.remove(self.tmpfile)


    def testRunSuccess(self):
        p = PythonScriptLauncher()
        p.sendCommand(self.tmpfile, 4)
        
        self.assertFalse(p.globalVariables.has_key('a'))
        self.assertEqual(p.localVariables['a'],1)
        self.assertEqual(p.localVariables['b'],2)
        
        out = p.readOutput()
        self.assertEqual(out,'Starting...\nFinishing...\n')
                

    def testRunFailTimeOut(self):
        p = PythonScriptLauncher()
        p.sendCommand(self.tmpfile, 0.1)
        
        self.assertFalse(p.globalVariables.has_key('a'))
        self.assertEqual(p.localVariables['a'],1)
        self.assertFalse(p.localVariables.has_key('b'))
        
        out = p.readOutput()
        self.assertEqual(out,None)
    
    def testRunSuccesAndFail (self):
        p = PythonScriptLauncher()
        
        p.sendCommand(self.tmpfile, 4)
        self.assertFalse(p.globalVariables.has_key('a'))
        self.assertEqual(p.localVariables['a'],1)
        self.assertEqual(p.localVariables['b'],2)
        out = p.readOutput()
        self.assertEqual(out,'Starting...\nFinishing...\n')
        
        p.resetAndSendCommand(self.tmpfile, 0.1)
        self.assertFalse(p.globalVariables.has_key('a'))
        self.assertEqual(p.localVariables['a'],1)
        self.assertFalse(p.localVariables.has_key('b'))
        
        
        
  
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()