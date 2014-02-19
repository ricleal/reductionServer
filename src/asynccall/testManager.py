'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import os

from asynccall.manager import LaunchManager

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


    def testLauncherNotThrows(self):
        m = LaunchManager()
        m.sendCommand(self.tmpfile, 2)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPython']
    unittest.main()