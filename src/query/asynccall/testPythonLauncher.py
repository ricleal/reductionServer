'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import os
import config.config

from pythonlauncher import PythonScriptLauncher

class Test(unittest.TestCase):

    tmpfile = '/tmp/test12324.py'
    tmpfile2 = '/tmp/test123242.py'
    tmpfile3 = '/tmp/test123243.py'

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

        f = open(self.tmpfile2, 'w')
        f.write("import time\n")
        f.write("print 'Starting...'\n")
        f.write("print 'input params', params\n")
        f.write("time.sleep(0.5)\n")
        f.write("result = {'out' : 1234}\n")
        f.write("print 'Finishing...'\n")
        
        f = open(self.tmpfile3, 'w')
        f.write("import time\n")
        f.write("print 'Starting...'\n")
        f.write("print '%{toreplace}' \n")
        f.write("print 'Finishing...'\n")



    def tearDown(self):
        os.remove(self.tmpfile)
        os.remove(self.tmpfile2)
        os.remove(self.tmpfile3)

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
        
        
    def testInputOutputParams(self):
        p = PythonScriptLauncher()
        params = {'param1' : 1234, 'param2' : 5678 }
        p.setInputParameters(params)
        p.sendCommand(self.tmpfile2, 4)
        out = p.readOutput()
        print out
        self.assertIn("{'param2': 5678, 'param1': 1234}", out)
        res = p.getResult()
        self.assertEqual(res,{'out' : 1234})
    
    def testSendCommandWithParams(self):
        p = PythonScriptLauncher()
        params = {'toreplace' : 'REPLACED' }
        p.sendCommand(self.tmpfile3, 4,params)
        out = p.readOutput()
        print out
        self.assertIn("REPLACED", out)
        
    def testRealScript(self):
        p = PythonScriptLauncher()
        params = {'datafile':'/net/serdon/illdata/131/in5/exp_TEST-2216/rawdata/104041.nxs'}
        p.sendCommand('/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py', 30,params)
        res = p.getResult()
        print res
        self.assertIn("data_values", res)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()