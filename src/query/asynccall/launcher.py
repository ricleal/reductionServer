'''
Created on Feb 18, 2014

@author: leal
'''
import subprocess
import threading
import time
import logging
import os
import abc
import tempfile
import pprint

logger = logging.getLogger(__name__)

class Launcher():
    '''
    
    Abstract General Launcher
     
    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, initParams=None):
        '''
        @param content: binary stream passed by post 
        '''
        logger.debug("Launcher init method...")
        
        self.__initParams = initParams 
       
    
    @abc.abstractmethod
    def sendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher keeping previous state
        @param command: is file
        @param inputParams: is json dict 
        '''
        return
    
    @abc.abstractmethod
    def resetAndSendCommand(self,command,timeout,inputParams=None):
        '''
        Sends a command to the launcher but before resets all the previous state
        '''
        return
    
    @abc.abstractmethod
    def readOutput(self):
        ''' reads stdout '''
        return       
    
    
    @abc.abstractmethod
    def run(self):
        '''
        Will be called by the methods above
        '''
        return
    
    
    def substituteParamsInFile(self,filename,paramsDict,suffix="",prefix="tmp"):
        '''
        Will replace occurences of
        %{key} for value 
        @return: new file with substitutions
        '''
        
        #logging.debug(pprint.pformat(paramsDict))
        
        ft = tempfile.NamedTemporaryFile(delete=False,suffix=suffix,prefix=prefix)
        try:
            with open(ft.name, 'w') as new_file:
                with open(filename, 'r') as f:
                    for line in f:
                        new_line = self._replaceAll(line, paramsDict)
                        new_file.write(new_line)
        except Exception, e:
            logger.exception(str(e))
        
        #logging.debug(pprint.pformat(open(ft.name).readlines()))
        return ft.name
    
    def _replaceAll(self, text, mydict):
        for k, v in mydict.iteritems():
            k = "%{" + k + "}"
            text = text.replace(k, v)
        return text
    
    
    def __str__(self):
        return self.__class__()
    
    def __repr__(self):
        return self.__str__()
    
    @abc.abstractmethod
    def getResult(self):
        '''
        Get result in form of json
        variable result
        '''
        return