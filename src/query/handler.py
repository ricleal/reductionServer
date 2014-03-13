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
import os.path
from config.config import configParser
import pprint
from query.asynccall.manager import LaunchManager
import threading

#from apt_pkg import config

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
                
                logger.debug("Build executable and params")
                inputParams = self._buildInputParams()
                queryJson['input_params'] = inputParams
            
                logger.debug("Insert query in the DB")
                self._storeInTheDB(queryJson)
                
                # This must be executed in thread!!
                t = threading.Thread(target=self._executeQueryInParallel, args=(inputParams,))
                t.start()
                ####
                                
                # Return
                successMessageStr = self.jsonSuccessTemplate%(self.queryId,
                                                              self.validator.timeout,
                                                              self.validator.executable)
                logger.debug("Message to send to the client:" + successMessageStr)
                
                return ast.literal_eval(successMessageStr)
            except Exception, e:
                message = "Problems while processing the query..."
                logger.exception(message  + str(e))
                return Messages.error(message, str(e));
          
    
    def _buildQuery(self):
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
    
    def _buildInputParams(self):
        '''
        Necessary input params for Lamp and Mantid
        Some redundancy is introduced as scripts read different formats
        '''
        params = {}
        params["instrument"] =  configParser.get("General", "instrument_name")
        
        if self.validator.jsonContent.has_key("params") :
            queryParams = self.validator.jsonContent["params"]
            if queryParams.has_key("numors"): # list of numors:
                listOfNumors =  queryParams["numors"]
                db = storage.getDBConnection()
                listOfFiles = db.getListOfFiles(listOfNumors)
                if len(listOfFiles) > 1:
                    params["data_files_full_path"]=listOfFiles
                    params["data_files"] = []
                    for i in listOfFiles:
                        b = os.path.basename(i)
                        params["data_files"].append(b)
                else:
                    params["data_file_full_path"]=listOfFiles[0]
                    params["data_file"] = os.path.basename(listOfFiles[0])
                # Assuming all files in the same folder
                params["working_path"] = os.path.dirname(listOfFiles[0])
        logger.debug(pprint.pformat(params))
        return params 
        
    def _launchTheExecutable(self, inputParams):
        logger.debug("Launching : " + self.validator.executable)
        m = LaunchManager()
        m.sendCommand(self.validator.executable, self.validator.timeout,inputParams)
        res = m.getResult()
        return res
    
    
    def _storeExecutableResults(self,resultingJson):
        queryJson = {}
        logger.debug("storeExecutableResults")
        logger.debug(resultingJson)
        queryJson["result"] = resultingJson
        queryJson["status"] = "done" 
        queryJson["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        queryJson["end_local_time"] = time.asctime(time.localtime(time.time()))
        
        db = storage.getDBConnection()
        db.updateQuery(self.queryId, queryJson)
    
    
    def _executeQueryInParallel(self,inputParams):
        logger.debug("Executing the query in parallel")
        resultingJson = self._launchTheExecutable(inputParams)
        logger.debug("Store results in the DB")
        self._storeExecutableResults(resultingJson)
        
        
        
        