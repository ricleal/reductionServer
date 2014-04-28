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
        os.remove(self.tmpfile2)
        os.remove(self.tmpfile3)

        
        
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
        params = {'data_file_full_path':'/net/serdon/illdata/131/in5/exp_TEST-2216/rawdata/104041.nxs'}
        p.sendCommand('/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py', 30,params)
        res = p.getResult()
        print res
        self.assertIn("data_values", res)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()