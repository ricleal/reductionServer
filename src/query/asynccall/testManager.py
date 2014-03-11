'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import os

from query.asynccall.manager import LaunchManager
from config.config import configParser

class Test(unittest.TestCase):

    scriptToCall = "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.py"
    
    def setUp(self):
        # Make sure Python launcher will be called
        configParser.set("Launcher", "name", "PythonScriptLauncher")
        

    def tearDown(self):
        pass

    def testLauncherNotThrows(self):
        m = LaunchManager()
        params = {"numors" : ["/home/leal/Documents/Mantid/IN5/094460.nxs"]}
        m.sendCommand(self.scriptToCall, 30)
        m.getResult()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPython']
    unittest.main()