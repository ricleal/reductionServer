'''
Created on Feb 19, 2014

@author: leal
'''
import unittest
import time
from shelllauncher import ShellLauncher
import config.config

class Test(unittest.TestCase):

    lampExecutable = '/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws'
    lampPrompt = "loaded ..."
    lampExitCommand = "exit"
    lampCleanupCommand = "wreset,all"
    stringToPrint = "Hello, Python"
    fullStartExecutable = [lampExecutable, 
                                    lampPrompt, lampExitCommand,lampCleanupCommand]

    tmpfile = '/tmp/test12324.prox'
    
    def setUp(self):
        f = open(self.tmpfile, 'w')
        f.write('print,"Line 1"\n')
        f.write('print,"Line 2"\n')
        f.write('print,"Line 3"\n')
        f.write('print,"Line 4"\n')
        f.write('RDSET,inst="D20"\n')
        f.write('P_SET_PATH,"/home/leal/Documents/Mantid/D20/"\n')
        f.write("w1=rdopr('829007',datp=d)\n")
        f.write("help, w1, /st\n")
        f.write('print,"Line 5"\n')
        f.write('print,"Line 6"\n')
        f.close()

    def tearDown(self):
        pass


    def testRunSuccess(self):
        p = ShellLauncher(self.fullStartExecutable)
        p.sendCommand(self.tmpfile, 30)
        out = p.readOutput()
        print out
        self.assertIn("Line 2", out.strip())
        p.exit()
        

        
    def testRealLamp(self):
        p = ShellLauncher(self.fullStartExecutable)
        out = p.readOutput()
        print out
                
        params = {'instrument' : 'D20',
                  'working_path' : '/home/leal/Documents/Mantid/D20/',
                  'data_file':'829007'}
        p.sendCommand('/home/leal/git/reductionServer/src/query/scripts/ILL_D20_tt2d.prox', 30,params)
        
        out = p.readOutput()
        print out
        
        res = p.getResult()
        print res

        self.assertIn("data_shape", res)
        
        p.exit()
        
    
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()