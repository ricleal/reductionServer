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
        @param content: binary stream - contents of the nexus file 
        '''
        
        logger.debug("Parsing request...")
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False, prefix='live_', suffix='.tmp')
        self.tempFile.write(content)
        self.tempFile.close()
        
        self.file = None

    def __del__(self):
        logger.debug("Deleting temporary file: %s" % self.tempFile.name)

        try :
            os.remove(self.tempFile.name)
        except  Exception as e:
            logger.error("Error removing temporary file: " + str(e))

    def filename(self):
        return self.tempFile.name
    
    def __repr__(self, *args, **kwargs):
        return self.filename()
    
    @abc.abstractmethod
    def isValid(self):
        return
    
    @abc.abstractmethod
    def openFile(self):
        return
    
    @abc.abstractmethod
    def closeFile(self):
        return
        

