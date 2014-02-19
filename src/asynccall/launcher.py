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


logger = logging.getLogger(__name__)

class Launcher(threading.Thread):
    '''
    
    Abstract General Launcher
     
    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, initParams=None):
        '''
        @param content: binary stream passed by post 
        '''
        logger.debug("Launcher init method...")
        
        threading.Thread.__init__(self)
        
        self.__initParams = initParams 
       
    
    @abc.abstractmethod
    def sendCommand(self,command,timeout):
        '''
        Sends a command to the launcher keeping previous state
        '''
        return
    
    @abc.abstractmethod
    def resetAndSendCommand(self,command,timeout):
        '''
        Sends a command to the launcher but before resets all the previous state
        '''
        return
    
    @abc.abstractmethod
    def readOutput(self):
        return
    
    
    @abc.abstractmethod
    def run(self):
        '''
        Will be called by the methods above
        '''
        return
    
    
    def __str__(self):
        return "Launcher class!"
    
    def __repr__(self):
        return self.__str__()
    
        
    