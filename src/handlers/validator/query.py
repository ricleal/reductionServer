'''
Created on Feb 24, 2014

@author: leal
'''
from data.messages import Messages
from handlers.query.definition import Query as QueryDefinition

import storage
import logging
import config.config
import json
import os.path

logger = logging.getLogger(__name__)

class QueryValidator(object):
    '''
    
    Class to Validate the queries received by the server.
    
    It will validate json, numors, etc
    
    
    
    '''

    jsonSuccessTemplate = """{
        'query_id' : '%s',
        'timeout' : '%d',
        'details' : %r
    }"""

    def __init__(self, content):
        '''
        Constructor
        
        content in the form of:
        
        
        '''
        self.rawContent = content
        
        self.jsonContent = None
        self.queryDef = QueryDefinition()
        
    
    def validateQuery(self):
        '''
        Main function
        
        @return: Json with queryId + timeout for this function
        '''
        try :
            self._validateJson()
            self._validateFunctionName()
            self._validateExecutable()
            
        
            # TODO
            # return jsonSuccessTemplate
        except Exception, e:
            message = "Problems while validating the query..."
            logger.exception(message  + str(e))
            return Messages.error(message, str(e));
            
    
    def _validateJson(self):
        try :
            self.jsonContent = json.loads(self.rawContent)
        except Exception, e:
            self.jsonContent = None
            raise Exception("JSON appears to be invalid.")
            logger.exception(str(e))
    
    def _validateFunctionName(self):
        
        method = self.jsonContent["method"]
        if not self.queryDef.doesLocalFunctionExist(method) :
            message = "Local Function does not exist: " + method
            raise Exception(message)
        if not self.queryDef.doesRemoteFunctionExist(method) :
            message = "Remote Function does not exist: " + method
            raise Exception(message)
            
    def _validateExecutable(self):
        method = self.jsonContent["method"]
        executable = self.queryDef.getExecutableFullPath(method)
        if not os.path.isfile(executable):
            message = "Executable not exist: " + executable
            raise Exception(message)
            
            
            
    
        
        
    