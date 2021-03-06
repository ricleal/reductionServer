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
import tempfile
from query.scripts.fix_lamp_json import fixPlot1D
from threading import Thread

logger = logging.getLogger(__name__) 
# logger.addHandler(logging.StreamHandler()) 
# logger.setLevel(logging.DEBUG)

class ShellLauncher(Launcher,Thread):
    '''
    
    
    '''
    
    def __init__(self, command):
        '''
        @param command: [_executable,_prompt,_exitCommand,_cleanUpCommand] 
        '''    
        logger.debug("Creating Shell Launcher.")
        Thread.__init__(self)
        Launcher.__init__(self)
        
    
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
        
        self._params = None
        self._result = None
        self._resultFile = None
    
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
        time.sleep(0.1)
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

    
    def sendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher keeping previous state
        '''
        self.timeout = timeout
        self.command = command
        self.inputParams = self._addTempFileToInputParams(inputParams)
        self._launch()
        
    def resetAndSendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher but before resets all the previous state
        '''
        self.timeout = timeout
        self.command = command
        self.inputParams = self._addTempFileToInputParams(inputParams)
        # reset
        self.send(self._cleanUpCommand)
        self._launch()

   
    def _addTempFileToInputParams(self,inputParams):
        if inputParams is None:
            inputParams = {}
        self._resultFile = tempfile.NamedTemporaryFile(delete=False,prefix="live_",suffix=".json").name
        inputParams["result_file"] = self._resultFile
        return inputParams
   
    def _launch(self):
        """
        
        Blocks the execution!!!!
        
        """
        if self.inputParams is not None :
            logger.debug("Old file: " + self.command)
            self.command = self.substituteParamsInFile(self.command,self.inputParams,prefix="live_",suffix=".prox")
            logger.debug("New file: " + self.command)
        
        # Assuming only files are passed to lamp
        self.command = "@"+self.command
        
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.command )
            self.__process.terminate()
            self.join()
            logger.debug("Done.")
        else :
            logger.info("Thread finished successfully: %s"%self.command)
        
        if self.inputParams is not None and self.command.startswith('/tmp'):
            os.remove(self.command)
        self.inputParams = None
        
        
        
        # Restart thread to avoid : raise RuntimeError("threads can only be started once")
        super(ShellLauncher, self).__init__()
    
        
    
    def run(self):
        '''
        Overrides: threading.Thread
        
        Executed through a thread
        
        Communicate  blocks until the command is fully executed.
        '''
        
        logger.debug("Running in background: %s" % self.command)        
        
        time.sleep(0.1)
        self.send(self.command)
        # Needs hight time out otherwise don't write to the file!
        time.sleep(10)
    
    def readOutput(self):
        return self.receiveOutput()
        
    def send(self,command):
        self._relaunchIfItIsNotRunning()
        commandSent=command + os.linesep
        self.__process.stdin.write(commandSent)        
        self.__process.stdin.flush()        
        logger.debug("Command sent to shell: " + commandSent)
    
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
        logger.debug('Exiting shell launcher...')
    
    def __del__(self):
        if self._isSubProcessRunning() :
            self.exit()    
    
    
    #TODO
    def setInputParameters(self,inputParams=None):
        '''
        Sets input parameters
        variable params in json
        '''
        self._params = inputParams
        
    
    #TODO
    def getResult(self):
        '''
        Get result in form of json
        variable result
        '''
        
        if self._resultFile is not None:
            try:
                logger.debug("Temporary file with resulting json: %s"%self._resultFile)
                with open(self._resultFile, 'r') as read_file:
                    contents = read_file.read()
                if len(contents) <= 0 :
                    raise Exception("Results file appears to be empty!")
                self._result = fixPlot1D(contents)
                os.remove(self._resultFile)
            except Exception, e:
                logger.exception(str(e))
                self._result = None
        
        return self._result
        
    



        
    

