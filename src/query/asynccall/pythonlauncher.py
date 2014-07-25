'''
Created on Feb 18, 2014

@author: leal
'''

from launcher import Launcher

import logging
import sys
import StringIO
import contextlib
import os
from multiprocessing import Process, Queue

logger = logging.getLogger(__name__) 

    

class PythonScriptLauncher(Launcher,Process):
    '''
    
    The python launcher 
    USE:
    globalVariables
    localVariables
    To keep a thread in the execution!
    
    
    The script send as command should read variables:
    param - input parameters
    set the result as 
    result - variable
    
    
    '''
    
    def __init__(self, initParams=None):
        '''
        
        '''    
        logger.debug("Creating Python Script Launcher...")
        
        
        Process.__init__(self)
        Launcher.__init__(self, initParams)
        
        self.globalVariables= {}
        self.localVariables= {}
        
        self.queueResult = Queue()
        self.queueOutput = Queue()
        
        self.localVariables = {}
        self.globalVariables = {}
        self.result = None
        self.output = None
        
        self.timeout = None
        self.command = None
    
    @contextlib.contextmanager
    def _stdoutIO(self,stdout=None):
        '''
        Redirects standard output
        '''
        old = sys.stdout
        if stdout is None:
            stdout = StringIO.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
    
    def sendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher keeping previous state
        '''
        self.timeout = timeout
        self.command = command
        self.inputParams = inputParams
        self._launch()
        
    def resetAndSendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher but before resets all the previous state
        '''
        self.timeout = timeout
        self.command = command
        self.inputParams = inputParams
        self._launch()
    
    # private
    def _launch(self):
        """
        Blocks the execution!!!!
        """
        if self.inputParams is not None :
            logger.debug("Old file: " + self.command)
            self.command = self.substituteParamsInFile(self.command,self.inputParams,suffix=".py",prefix="live_")
            logger.debug("New file: " + self.command)
        
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.command )
            self.terminate()
            self.join()
        else :
            logger.info("Thread finished successfully: %s"%self.command)
        
        if self.inputParams is not None and self.command.startswith('/tmp'):
            logger.info("Deleting file: " + self.command)
            os.remove(self.command)
        self.inputParams = None
        
        # Restart thread to avoid : raise RuntimeError("threads can only be started once")
        #super(PythonScriptLauncher, self).__init__()
    
    
    def run(self):
        '''
        No memory sharing!
        '''
        logger.debug("Running in background: %s" % self.command)        
        
        with self._stdoutIO() as s:
            execfile(self.command, self.globalVariables, self.localVariables)
        self.queueOutput.put(s.getvalue())
        
        result = {}
        if self.localVariables.has_key('result') :
            result = self.localVariables['result']
        self.queueResult.put(result)
        
    def readOutput(self):
        return self.queueOutput.get(block=False)
    
    def setInputParameters(self,inputParams):
        '''
        Sets input parameters
        variable params
        '''
        self.localVariables['params'] = inputParams
    
    
    def getResult(self):
        '''
        Get result in form of json
        variable result
        '''
        return self.queueResult.get(block=False)
    
        
    
    ### Non private methods:
    
    


    