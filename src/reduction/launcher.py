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
import os

logger = logging.getLogger(__name__) 

class Launcher(threading.Thread):
    '''
    Launcher class
    
    Inherits from Thread.
    
    
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
        self.__pid = None
    
    def run(self):
        '''
        Overrides: threading.Thread
        
        Executed through a thread
        
        Communicate  blocks until the command is fully executed.
        '''
        
        self.__startTime = time.time()

        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__pid = self.__process.pid
        
        self.__out, self.__err = self.__process.communicate()
    
    def __isTimedOut(self):
        elapsedTime =  time.time() - self.__startTime
        timer = self.__timeout - elapsedTime 
        if timer < 0: 
            return True
        else:
            return False
            
    ### Non private methods:
    
    def execute(self):
        '''
        Doesn't block!!! Runs the command in background.
        '''
        logger.debug("Running in background: %s" % self.__command)
        self.start() 
    
    def wait(self):
        '''
        Blocks until the process finishes or timeout
        '''
        if not self.__isTimedOut():
            logger.debug("Waiting for the process to finish or to timeout...")
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
            logger.debug("Process finished or Timed out, but it is still alive... Killing it!")
            self.__process.terminate()
            self.join()
    
    def isSubProcessRunning(self):
        """
        Just checks if the subprocess is still running or timed out.
        If it's timeout kills it! 
        
        Assuming it's running. Otherwise we need some safety checks!
        """
        
        # Check if child process has terminated. Set and return returncode attribute.
        if self.__process.poll() is None:
            # still running:
            if self.__isTimedOut():
                if self.is_alive():
                    logger.debug("Process finished or Timed out, but it is still alive... Killing it!")
                    self.__process.terminate()
                    self.join()
                return False
            return True
        else:
            return False
    
    def kill(self):
        if self.is_alive():
            logger.debug("Thread is alive... Killing subprocess!")
            self.__process.terminate()
            self.join()
        
    
    def pid(self):
        if self.__pid is not None:
            return self.__pid
        else:
            logger.error("SubProcess / Pid is None!")
    
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
        time.sleep(0.1)
        print "Doing something in launcher while command runs in bg..."
        pid = l.pid()
        os.system('ps -ef | grep %d'%pid)
        print "Pid of the subprocess:", pid
        time.sleep(0.9)
        self.assertTrue(l.isSubProcessRunning(), "Is subprocess running?")
        print "Still doing something in launcher while command runs in bg..."
        time.sleep(2)
        self.assertEqual(l.returnCode(),0)
    
    def test_e_realTimeOut(self):
        print
        data = {}
        data['command'] = 'sleep 10'
        data['timeout'] = 2
        
        l = Launcher(data['command'],data['timeout'])
        l.execute()
        time.sleep(0.1)
        
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        
        data['out'] = l.output()
        data['err'] = l.error() 
        data['retCode'] = l.returnCode()
        self.assertNotEqual(l.returnCode(),0)
        print data    
        
    def test_f_realSuccess(self):
        print
        data = {}
        data['command'] = 'sleep 2'
        data['timeout'] = 10
        
        l = Launcher(data['command'],data['timeout'])
        l.execute()
        time.sleep(0.1)
        
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        
        data['out'] = l.output()
        data['err'] = l.error() 
        data['retCode'] = l.returnCode()
        self.assertEqual(l.returnCode(),0)
        print data    
        
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    