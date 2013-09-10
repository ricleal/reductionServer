#!/usr/bin/python

'''
Created on Aug 9, 2013

@author: leal

Launcher to run shell commands.



'''
import subprocess
import threading
import time
import logging

logger = logging.getLogger(__name__) 

class Launcher(threading.Thread):
    '''
    Launcher class.
    Constructer gets the shell command as parameter.
    
    '''

    def __init__(self,command,timeout):
        '''
        Constructor
        @param command: Shell commands
        @param timeout: Timeout
         
        '''
        
        threading.Thread.__init__(self)
        self.__command = command
        self.__timeout = timeout
        logger.debug("Command to execute <%s> with timeout=%d"%(command,timeout))
        self.__out = None
        self.__err = None
        self.__process = None
        self.__startTime = None
    
    def run(self):
        '''
        Communicate  blocks until the command is fully executed
        Executed through a thread
        '''
        
        self.__startTime = time.time()

        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__out, self.__err = self.__process.communicate()
    
    def execute(self):
        '''
        Doesn't block!!! Runs the command in background.
        '''
        logger.debug("Running in background: %s" % self.__command)
        self.start()
    
    def wait(self):
        '''
        either wait for the process to finish
        or for the timeout
        '''
        elapsedTime =  time.time() - self.__startTime
        timeout = self.__timeout - elapsedTime 
        if timeout >0:
            logger.debug("Waiting for the process to finish with a timeout...")
            self.join(self.__timeout)
            logger.debug("Process finished...")
        # if after the timeout it is still alive
        if self.is_alive():
            logger.debug("Process is still alive... Killing it!")
            self.__process.terminate()
            self.join()
            
    
    def executeAndWait(self):
        '''
        Blocks until process executes or times out
        '''
        self.start()
        logger.debug("Waiting for the process to finish with a timeout...")
        self.join(self.__timeout)
        # if after the timeout it is still alive
        if self.is_alive():
            logger.debug("Timeout!! Process is still alive... Killing it!")
            self.__process.terminate()
            self.join()
    
    def isSubProcessRunning(self):
        if self.__process.poll() is None:
            return True
        else:
            return False
    
    def exit(self):
        self.__process.terminate()
        self.join()
            
    def error(self):
        return self.__err
    
    def output(self):
        return self.__out
    def returnCode(self):
        return self.__process.returncode

import unittest

class Test(unittest.TestCase):
    
    def setUp(self):
        from logging import config as _config
        _config.fileConfig('../logging.ini',disable_existing_loggers=False)
    

    def test_a_ShortCommandLongTimeoutSuccess(self):
        print
        l = Launcher('ls',2)
        l.executeAndWait()
        print "** Out:"
        print l.output()
        self.assertEqual(l.returnCode(),0)
    
    def test_b_ShortCommandLongTimeoutFailure(self):
        print
        l = Launcher('ls -la /root',2)
        l.executeAndWait()
        print "** Error:"
        print l.error()
        self.assertNotEqual(l.returnCode(),0)
    
    def test_c_LongCommandShortTimeout(self):
        print
        l = Launcher('sleep 10',1)
        l.executeAndWait()
        self.assertNotEqual(l.returnCode(),0)
    
    def test_d_AverangeCommandDoesntBlockCaller(self):
        print
        l = Launcher('sleep 2',10)
        l.execute()
        print "Doing something in launcher while command runs in bg..."
        time.sleep(1)
        self.assertTrue(l.isSubProcessRunning(), "Is subprocess running?")
        print "Still doing something in launcher while command runs in bg..."
        time.sleep(2)
        self.assertEqual(l.returnCode(),0)
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    