'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import time
from shelllauncher import ShellLauncher

class Test(unittest.TestCase):

    lampExecutable = '/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws'
    lampPrompt = "loaded ..."
    lampExitCommand = "exit"
    lampCleanupCommand = "wreset,all"
    stringToPrint = "Hello, Python"
    fullStartExecutable = [lampExecutable, 
                                    lampPrompt, lampExitCommand,lampCleanupCommand]

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testRunSuccess(self):
        p = ShellLauncher(self.fullStartExecutable)
        p.sendCommand('print, "%s"'%self.stringToPrint, 1)
        out = p.readOutput()
        self.assertEqual(out.strip(),self.stringToPrint)
        p.sendCommand('print, "%s"'%self.stringToPrint, 1)
        out = p.readOutput()
        self.assertEqual(out.strip(),self.stringToPrint)
        p.exit()
        
    def testReRun(self):
        p = ShellLauncher(self.fullStartExecutable)
        p.sendCommand('print, "%s"'%self.stringToPrint, 1)
        out = p.readOutput()
        self.assertEqual(out.strip(),self.stringToPrint)
        p.exit()
        p.sendCommand('print, "%s"'%self.stringToPrint, 1)
        out = p.readOutput()
        self.assertNotEqual(out.strip(),None)
        p.exit()
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()