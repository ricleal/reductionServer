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
    Launcher class. Inherits from Thread.
    
    Constructer gets the shell command as parameter.
    
    Every command is executed within a thread with a time out. Thus, it never blocks the execution.
    
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
        self.__pid = None
        self.__returnCode = None
    
    def run(self):
        '''
        Overrides: threading.Thread
        
        Executed through a thread
        
        Communicate  blocks until the command is fully executed.
        '''
        
        logger.debug("Running in background: %s" % self.__command)        

        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__pid = self.__process.pid
        self.__out, self.__err = self.__process.communicate()
        self.__returnCode = self.__process.returncode
        
    ### Non private methods:
    
    def launch(self):
        """
        Only function to be called. Starts the command with a time out.
        
        Block the execution!!!!
        
        It might have to be launched within other thread!!!!
        http://stackoverflow.com/questions/4158502/python-kill-or-terminate-subprocess-when-timeout
        """
        self.start()
        self.join(self.__timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.__command )
            self.__process.terminate()
            self.join()
            logger.debug("Done.")
        else :
            logger.info("Thread finished successfully: %s"%self.__command)
    
    def isSubProcessRunning(self):
        """
        Just checks if the thread is running.
        """    
        # Check if child process has terminated. Set and return returncode attribute.
        if self.__process.poll() is None:
            return True
        else:
            return False
    
    def kill(self):
        if self.is_alive():
            logger.debug("Thread is alive... Killing subprocess: %s"%self.__command)
            self.__process.terminate()
            self.join()
            logger.debug("Process killed...")
        
    
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
        return self.__returnCode
    
    def __del__(self):
        self.kill()

import unittest

class Test(unittest.TestCase):
    
    def setUp(self):
        from logging import config as _config
        _config.fileConfig('../logging.ini',disable_existing_loggers=False)
    

    def test_a_ShortCommandLongTimeoutSuccess(self):
        print
        l = Launcher('ls',2)
        l.launch()
        print "** Out:"
        print l.output()
        self.assertEqual(l.returnCode(),0)
    
    def test_b_ShortCommandLongTimeoutFailure(self):
        print
        l = Launcher('ls -la /root',2)
        l.launch()
        print "** Error:"
        print l.error()
        self.assertNotEqual(l.returnCode(),0)
    
    def test_c_LongCommandShortTimeout(self):
        print
        l = Launcher('sleep 10',1)
        l.launch()
        self.assertNotEqual(l.returnCode(),0)
        
    
    def test_d_AverangeCommandDoesntBlockCaller(self):
        print
        
        l = Launcher('sleep 2',10)
        
        # As launch block execution let's run in in a thread
        t = threading.Thread(target=l.launch)
        t.start()
        
        print "Doing something in launcher while command runs in bg..."
        time.sleep(0.1)
        pid = l.pid()
        os.system('ps -ef | grep %d'%pid)
        print "Pid of the subprocess:", pid
        time.sleep(0.5)
        self.assertTrue(l.isSubProcessRunning(), "Is subprocess running?")
        print "Still doing something in launcher while command runs in bg..."
        time.sleep(2)
        self.assertEqual(l.returnCode(),0)
        
        t.join()
    
    def test_e_realTimeOut(self):
        print
        data = {}
        data['command'] = 'sleep 10'
        data['timeout'] = 2
        
        l = Launcher(data['command'],data['timeout'])
        t = threading.Thread(target=l.launch)
        t.start()
        time.sleep(0.1)
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        t.join()
        
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
        t = threading.Thread(target=l.launch)
        t.start()
        time.sleep(0.1)
        
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        t.join()
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
    