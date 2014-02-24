'''
Created on Feb 24, 2014

@author: leal
'''
from handlers.content.manager import Manager  
from data.messages import Messages
import storage
import logging
import config.config

logger = logging.getLogger(__name__)

class FileValidator(object):
    '''
    classdocs
    '''


    def __init__(self, content):
        '''
        Constructor
        '''
        self.content = content
    
    def validateFile(self,numor):
        handlerManager = Manager(self.content)
        fileHandler = handlerManager.getRespectiveHandler()
        if fileHandler is None:
            return Messages.error("File/URL received is not valid.", "Neither ASCII, Nexus nor valid URL.");
        else:
            db = storage.getDBConnection()
            db.insertOrUpdateNumor(numor, fileHandler.filename())
            return Messages.success("File/URL successfully received.", "The handlers is: " + fileHandler.__class__.__name__)

        