'''
Created on Feb 24, 2014

@author: leal
'''

from query.specs.definition import QuerySpecs
from data.messages import Messages

import logging
import config.config
import json
import os.path
import storage

logger = logging.getLogger(__name__)

class QueryValidator(object):
    '''
    
    Class to Validate the queries received by the server.
    
    It will validate json, numors, etc
        
    '''



    def __init__(self, content):
        '''
        Constructor
        
        content in the form of:
        
        
        '''
        self._rawContent = content
        self.queryDef = QuerySpecs()
        
        # variables
        self.jsonContent = None
        self.executable = None
        self.timeout = None
        self.numors = []
        
    def validateQuery(self):
        '''
        Main function
        
        @return: Json with queryId + timeout for this function
        '''
        try :
            self._validateJson()
            self._validateFunctionName()
            self._validateExecutableAndTimeOut()
#             self._validateNumors()
            # return None if no problems
            return None
        
        except Exception, e:
            message = "Problems while validating the query..."
            logger.exception(message  + str(e))
            return Messages.error(message, str(e));
            
    
    def _validateJson(self):
        try :
            self.jsonContent = json.loads(self._rawContent)
        except Exception, e:
            self.jsonContent = None
            raise Exception("JSON appears to be invalid.")
            logger.exception(str(e))
    
    def _validateFunctionName(self):
        
        method = self.jsonContent["method"]
        if not self.queryDef.doesFunctionExist(method) :
            message = "Function is not defined in the specs file: " + method
            raise Exception(message)
        
            
    def _validateExecutableAndTimeOut(self):
        method = self.jsonContent["method"]
        self.executable = self.queryDef.getExecutableFullPath(method)
        if not os.path.isfile(self.executable):
            message = "Executable not exist: " + self.executable
            raise Exception(message)
        self.timeout = self.queryDef.getExecutableTimeout(method)
        if self.timeout is None:
            message = "Timeout does not exist for " + method
            raise Exception(message)
            
            
#     def _validateNumors(self):
#         numorsList=[]
#         if self.jsonContent.has_key("params") :
#             listOfParams = self.jsonContent["params"];
#             for i in listOfParams:
#                 if i.has_key("numors"):
#                     numorsList = i["numors"]
#         if len(numorsList) > 0 :
#             db = storage.getDBConnection()
#             l = db.getListOfAllNumors()
            
        
            
    
        
        
    