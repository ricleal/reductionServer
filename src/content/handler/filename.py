'''
Created on Nov 22, 2013

@author: leal
'''

import abc
import logging
import tempfile
import os

from content.handler.handler import Handler

logger = logging.getLogger(__name__)

class File(Handler):
    '''
    
    Abstract General Handler for threat files sen to the server 
    '''
    __metaclass__ = abc.ABCMeta
    
    
    def __init__(self, content,suffix='.tmp'):
        '''
        @param content: binary stream - contents of the nexus file 
        '''
        
        logger.debug("File content init method...")
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False, prefix='live_', suffix=suffix)
        self.tempFile.write(content)
        self.tempFile.close()
        
        logger.debug("Content written to: %s" % self.tempFile.name)
        self.file = None

    def __del__(self):
#         logger.debug("Deleting temporary file: %s" % self.tempFile.name)
# 
#         try :
#             os.remove(self.tempFile.name)
#         except  Exception as e:
#             logger.error("Error removing temporary file: " + str(e))
        pass

    def filename(self):
        return self.tempFile.name
    
    
    @abc.abstractmethod
    def isValid(self):
        return
    
    @abc.abstractmethod
    def openFile(self):
        return
    
    @abc.abstractmethod
    def closeFile(self):
        return
        

