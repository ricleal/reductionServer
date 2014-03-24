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
        self._functionsRemoteFilename = configParser.get("General", "functions_remote_specs_file")
        self._instrumentName = configParser.get("General", "instrument_name")
    
    def _getAllMethodsAsText(self):
        
        with open(self._functionsRemoteFilename, 'r') as content_file:
            content = content_file.read()
        return content
        
    
    def getAllMethods(self):
        logger.debug("Getting methods...")
        content = self._getAllMethodsAsText()
        contentAsDic = None
        try :
            contentAsDic = ast.literal_eval(content)
        except Exception, e:
            message = "The remote specs file does not appear to have a json format."
            logger.exception(message  + str(e))
            contentAsDic = Messages.error(message, str(e), self._functionsRemoteFilename );
        return contentAsDic
    
    def getMethodsForThisInstrument(self):
        logger.debug("Getting methods...")
        content = self._getAllMethodsAsText()
        contentAsDic = None
        res = {}
        try :
            contentAsDic = ast.literal_eval(content)
            for k in contentAsDic.keys():
                if isinstance(contentAsDic[k],dict):
                    thisEntry = contentAsDic[k]
                    if thisEntry.has_key('instruments'):
                        if self._instrumentName in thisEntry['instruments']:
                            res[k]=contentAsDic[k]
        except Exception, e:
            message = "The remote specs file does not appear to have a json format."
            logger.exception(message  + str(e))
            res = Messages.error(message, str(e), self._functionsRemoteFilename );
        return res
    


    
        