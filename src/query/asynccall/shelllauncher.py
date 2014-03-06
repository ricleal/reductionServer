'''
Created on Feb 18, 2014

@author: leal
'''


from launcher import Launcher

import logging
import Queue
import subprocess
import time
import os
import threading

logger = logging.getLogger(__name__) 
# logger.addHandler(logging.StreamHandler()) 
# logger.setLevel(logging.DEBUG)

class ShellLauncher(Launcher):
    '''
    
    
    '''
    
    def __init__(self, command):
        '''
        @param command: [_executable,_prompt,_exitCommand,_cleanUpCommand] 
        '''    
        logger.debug("Creating Shell Launcher.")
        super(ShellLauncher, self).__init__()
    
        self._executable = command[0]
        self._prompt =  command[1]
        self._exitCommand =  command[2]
        self._cleanUpCommand = command[3]
        
        self.__out = None
        self.__err = None
        self.__process = None
        self.__pid = None
        self.__returnCode = None
        
        self._launchProcess()
        
        self._outQueue = Queue.Queue()
        self._errQueue = Queue.Queue()

        self._startThreads()
        self._startExecutable()
    
    def _launchProcess(self):
        logger.debug('Starting subprocess...')
        self.__process = subprocess.Popen(self._executable,
                              shell=True, universal_newlines=True, stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__pid = self.__process.pid
        logger.debug('Started subprocess with pid : %d'%self.__pid)
 
    def _startThreads(self):
        logger.debug('Starting Queues...')
        self.outThread = threading.Thread(target=self._enqueueOutput, args=(self.__process.stdout, self._outQueue))
        self.errThread = threading.Thread(target=self._enqueueOutput, args=(self.__process.stderr, self._errQueue))
        
        self.outThread.daemon = True
        self.errThread.daemon = True
        
        self.outThread.start()
        self.errThread.start()
    
    def _startExecutable(self):
        '''
        Starts the command until _prompt appears
        '''
        logger.debug(self._executable + 'is starting...')
        output = self._getOutput(self._outQueue)
        while output.find(self._prompt) < 0:
            time.sleep(0.2)
            output = self._getOutput(self._outQueue)
        logger.debug(self._executable + 'is starting... Done!')
        
        errors = self._getOutput(self._errQueue)
        if len(errors.strip())>0: 
            logger.error(errors)
        

    def _enqueueOutput(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
    
    def _getOutput(self, outQueue):
        outStr = ''
        try:
            while True:  # Adds output from the Queue until it is empty
                outStr += outQueue.get_nowait()
        except Queue.Empty:
            return outStr
    
    def _relaunchIfItIsNotRunning(self):
        if not self._isSubProcessRunning():
            logger.debug('Relaunching subprocess...')
            self._launchProcess()
            self._outQueue = Queue.Queue()
            self._errQueue = Queue.Queue()   
            self._startThreads()
            self._startExecutable()
    
    def _isSubProcessRunning(self):
        """
        Just checks if the thread is running.
        """    
        # Check if child process has terminated. Set and return returncode attribute.
        if self.__process.poll() is None:
            return True
        else:
            return False

    
    def sendCommand(self,command,timeout):
        '''
        Sends a command to the launcher keeping previous state
        '''
        self.timeout = timeout
        self.command = command
        self._launch()
        
    def resetAndSendCommand(self,command,timeout):
        '''
        Sends a command to the launcher but before resets all the previous state
        '''
        self.timeout = timeout
        self.command = command
        # reset
        self.send(self._cleanUpCommand)
        self._launch()

   
    def _launch(self):
        """
        
        Blocks the execution!!!!
        
        """
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.command )
            self.__process.terminate()
            self.join()
            logger.debug("Done.")
        else :
            logger.info("Thread finished successfully: %s"%self.command)
        
        # Restart thread to avoid : raise RuntimeError("threads can only be started once")
        super(ShellLauncher, self).__init__()
    
        
    
    def run(self):
        '''
        Overrides: threading.Thread
        
        Executed through a thread
        
        Communicate  blocks until the command is fully executed.
        '''
        
        logger.debug("Running in background: %s" % self.command)        
        
        self.send(self.command)
        time.sleep(0.1)
    
    def readOutput(self):
        return self.receiveOutput()
        
    def send(self,command):
        self._relaunchIfItIsNotRunning()
        self.__process.stdin.write(command + os.linesep)        
        self.__process.stdin.flush()        
    
    def receiveOutput(self):
        output = self._getOutput(self._outQueue)
        return output
    
    def receiveErrors(self):
        errors = self._getOutput(self._errQueue)
        return errors
    
    def communicate(self,command,waitTimeForTheCommandToGiveOutput=0.2):
        logger.debug('Executing: ' + command)
        self.send(command)
        time.sleep(waitTimeForTheCommandToGiveOutput)
        return [self.receiveOutput(),self.receiveErrors()]
    
    def exit(self):
        """
        Try to send the exit command to subprocess running.
        Kill it if it is still running
        """
        if self._isSubProcessRunning() and self._exitCommand is not None:
            self.__process.stdin.write(self._exitCommand)
            self.__process.stdin.write(os.linesep)
            self.__process.stdin.flush()
            time.sleep(0.5)
        
        if self._isSubProcessRunning() :
            self.__process.kill()
        time.sleep(0.1)
        print 'Done!'
    
    def __del__(self):
        if self._isSubProcessRunning() :
            self.exit()    
    
    
        
    



        
    

