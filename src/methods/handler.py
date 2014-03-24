'''
Created on Mar 13, 2014

@author: leal
'''

import config.config
import logging
from data.messages import Messages
import simplejson
from config.config import configParser
import ast

logger = logging.getLogger(__name__)

class HandlerMethods(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def getMethods(self):
        logger.debug("Getting methods...")
        
        functionsRemoteFilename = configParser.get("General", "functions_remote_specs_file")
        with open(functionsRemoteFilename, 'r') as content_file:
            content = content_file.read()
        contentAsDic = None
        try :
            contentAsDic = ast.literal_eval(content)
        except Exception, e:
            message = "The remote specs file does not appear to have a json format."
            logger.exception(message  + str(e))
            contentAsDic = Messages.error(message, str(e), functionsRemoteFilename );
        return contentAsDic
    
    
        