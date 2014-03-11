'''
Created on Mar 7, 2014

@author: leal
'''

from query.validator.queryval import QueryValidator
from data.messages import Messages

import uuid
import ast
import datetime
import time
import storage
import logging

logger = logging.getLogger(__name__)

class QueryHandler(object):
    '''
    classdocs
    '''

    jsonSuccessTemplate = """{
        'query_id' : '%s',
        'timeout' : %d,
        'details' : %r
    }"""

    def __init__(self, content):
        '''
        Constructor
        '''
        self.validator = QueryValidator(content)
    
    def process(self):
        
        errors = self.validator.validateQuery()
        if errors is not None:
            logger.error("Problems while validating the query...")
            return errors
        else:
            try :
                logger.debug("Build query json")
                self.queryId = str(uuid.uuid4())
                queryJson = self._buildQuery()
                
                # TODO : 
                logger.debug("Build executable")
                executable = self._buildExecutableWithParams(self)
                
                # TODO : 
                logger.debug("Executing the query")
                resultingJson = self._launchTheExecutable(executable)
                
                logger.debug("Insert query in the DB")
                self._storeInTheDB(self,queryJson)
                
                logger.debug("Store results in the DB")
                self._storeExecutableResults(resultingJson)
                
                # Return
                successMessageStr = self.jsonSuccessTemplate%(self.queryId,
                                                              self.validator.timeout,
                                                              self.validator.executable)
                return ast.literal_eval(successMessageStr)
            except Exception, e:
                message = "Problems while processing the query..."
                logger.exception(message  + str(e))
                return Messages.error(message, str(e));
          
    
    def _buildQuery(self,queryId):
        queryJson = {}
        queryJson["queryId"] = self.queryId
        queryJson["start_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        queryJson["start_local_time"] = time.asctime(time.localtime(time.time()))
        queryJson["status"] = "running" 
        queryJson["executable"] = self.validator.executable
        queryJson["timeout"] = self.validator.timeout
        return queryJson
    
    def _storeInTheDB(self,queryJson):
        db = storage.getDBConnection()
        db.insertQuery(queryJson)
    
    def _buildExecutableWithParams(self):
        if self.validator.jsonContent.has_key("params") :
            queryParams = self.validator.jsonContent["params"]
            if queryParams.has_key("numors"): # list of numors:
                
                
            
        
    def _launchTheExecutable(self, executable):
        pass
    
    
    def _storeExecutableResults(self,resultingJson):
        queryJson = {}
        try:
            queryJson["result"] = ast.literal_eval(resultingJson)
        except Exception, e:
            message = "JSON of the output processing file looks invalid: " + str(e)
            logger.exception(message)
            logger.debug(resultingJson)
            queryJson["output"] = Messages.error(message,str(e))
        
        queryJson["status"] = "done" 
        queryJson["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        queryJson["end_local_time"] = time.asctime(time.localtime(time.time()))
        
        db = storage.getDBConnection()
        db.updateQuery(self.queryId, queryJson)
    
    
        
        
        
        
        