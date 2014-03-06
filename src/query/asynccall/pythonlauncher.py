'''
Created on Feb 18, 2014

@author: leal
'''

from launcher import Launcher

import logging
import sys
import StringIO
import contextlib

logger = logging.getLogger(__name__) 

    

class PythonScriptLauncher(Launcher):
    '''
    
    The python launcher 
    USE:
    globalVariables
    localVariables
    To keep a thread in the execution!
    
    
    '''
    
    def __init__(self, initParams=None):
        '''
        
        '''    
        logger.debug("Creating Python Script Launcher...")
        super(PythonScriptLauncher, self).__init__()
        
        self.setDaemon(True) # kills substreads when exit
        self.globalVariables= {}
        self.localVariables= {}
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
        self.globalVariables = {}
        self.localVariables = {}
        self._launch()
    
    # private
    def _launch(self):
        """
        Blocks the execution!!!!
        """
        
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.command )
        else :
            logger.info("Thread finished successfully: %s"%self.command)
        
        # Restart thread to avoid : raise RuntimeError("threads can only be started once")
        super(PythonScriptLauncher, self).__init__()
    
    
    def run(self):
        '''
        Overrides: threading.Thread
        Communicate  blocks until the command is fully executed.
        '''
        
        logger.debug("Running in background: %s" % self.command)        
        
        with self._stdoutIO() as s:
            execfile(self.command,  self.globalVariables, self.localVariables)
        self.output = s
        
        
    def readOutput(self):
        if self.output is None:
            return None
        else:
            return self.output.getvalue()
    
        
    ### Non private methods:
    
    


    