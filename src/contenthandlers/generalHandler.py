'''
Created on Nov 22, 2013

@author: leal
'''

import abc
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

class GeneralHandler(object):
    '''
    
    Abstract General Handler for threat files sen to the server 
    '''
    __metaclass__ = abc.ABCMeta
    
    
    def __init__(self, content):
        '''
        @param content: binary stream passed by post 
        '''
        logger.debug("General handler init method...")
        
    #         /self.file = None;
    
    def __repr__(self, *args, **kwargs):
        return self.filename()
    
    @abc.abstractmethod
    def filename(self):
        return
    
    @abc.abstractmethod
    def isValid(self):
        return
            

