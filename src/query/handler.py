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
    Main class to handle the query sent by the client.
    
    One object per query!!
    
    '''

    jsonSuccessTemplate = """{
        'query_id' : '%s',
        'timeout' : %d,
        'details' : %r
    }"""

    def __init__(self, content):
        '''
        builds a validator first
        '''
        self.validator = QueryValidator(content)
    
    def process(self):
        '''
        validates query first, if no errors:
        - build query fields : add key,value entries
        - insert query into the DB
        - launch it in a separate thread (thread runs until finishes or timeout!)
        '''
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
                # Add default values to the params
                self._buildDefaultParams(inputParams)
                queryJson['input_params'] = inputParams
            
                logger.debug("Insert query in the DB")
                self._storeInTheDB(queryJson)
                
                # _executeQueryInParallel(...) handles the system call
                t = threading.Thread(target=self._executeQueryInParallel, args=(inputParams,))
                t.start()
                                
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
        '''
        Add complementary fields to the query
        Note: Query is stored in the DB as json!
        '''
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
        Necessary input params for Lamp and Mantid.
        The json query has usually the following structure:
        {
            "method" : "theta_vs_counts",
            "params" : {
                "numors" : "94460"
            }
        }
        
        This routine 
        - split the numors from text into a list
        - Check if numors are in the DB (i.e. if a path file entry exists!)
        introduces the following fields:
        - data_files_full_path
        - data_files
        or the following 2:
        - data_file_full_path
        - data_file
        - working_path
        Some redundancy is introduced as scripts read different formats.
        
        TODO:
        More fields may be needed in the future!
        
        '''
        
        params = {}
        params["instrument"] =  configParser.get("General", "instrument_name")
        
        if self.validator.jsonContent.has_key("params") :
            queryParams = self.validator.jsonContent["params"]
            # for all paramms: 
            for key, value in queryParams.iteritems():
                if key.endswith("numors"):
                    listOfNumorsText =  value
                    # TODO : We have to handle this for numor ranges
                    listOfNumors = listOfNumorsText.split(',')
                    db = storage.getDBConnection()
                    listOfFiles = db.getListOfFiles(listOfNumors)
                    if len(listOfFiles) <= 0:
                        raise Exception("The numors %s don't exist in the DB"%listOfNumors)

                    params["working_path"] = os.path.dirname(listOfFiles[0])
                params[key]=value
        logger.debug(pprint.pformat(params))
        return params 
    
    def _buildDefaultParams(self, queryParams):
        """
        It will add to the @queryParams the default parameters,
        i.e., if a parameter is not present in  queryParams,
        the default { name : value } will be added
        
        @param queryParams : dic with { name : value, ... } of the input parameters
        """
        # Those are the default values 
        defaultParamsDic = self.validator.queryDef.getDefaultParameters("reduce")
        
        for key in defaultParamsDic:
            if key not in queryParams.keys():
                queryParams.update({ key : defaultParamsDic[key] })
        
            
        
    def _launchTheExecutable(self, inputParams):
        logger.debug("Launching : " + self.validator.executable)
        m = LaunchManager()
        m.sendCommand(self.validator.executable, 
                      self.validator.timeout,
                      inputParams)
        res = m.getResult()
        return res
    
    
    def _storeExecutableResults(self,resultingJson):
        queryJson = {}
        logger.debug("storing results of the routine in the Database. Query id = " + self.queryId )
        logger.debug(pprint.pformat(resultingJson))
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
        
        
        
        