'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import os

import config.config

from query.asynccall.manager import LaunchManager
from config.config import configParser

class Test(unittest.TestCase):
    
    def setUp(self):
        # Make sure Python launcher will be called
        configParser.set("Launcher", "name", "PythonScriptLauncher")
        

    def tearDown(self):
        pass

    def testLauncherNotThrows(self):
        m = LaunchManager()
        params = {'data_file_full_path':'/net/serdon/illdata/131/in5/exp_TEST-2216/rawdata/104041.nxs'}
        m.sendCommand('/home/leal/git/reductionServer/src/query/scripts/ILL_IN5_theta_vs_counts.py', 30, params)
        res = m.getResult()
        print res
        self.assertIn("data_values", res)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPython']
    unittest.main()
