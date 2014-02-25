'''
Created on Feb 24, 2014

@author: leal
'''

import logging
from config.config import configParser
import json

logger = logging.getLogger(__name__) 

class Query(object):
    '''
    classdocs
    
    Class responsable for storing the available functions:
    - Local
    - Remote (available to nomad)
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        functionsRemoteFilename = configParser.get("General", "functions_remote_specs_file")
        functionsLocalFilename = configParser.get("General", "functions_local_specs_file")
        
        self._functionsRemoteDic = self._importJsonFromFile(functionsRemoteFilename)
        self._functionsLocalDic = self._importJsonFromFile(functionsLocalFilename)
    
    def _importJsonFromFile(self,filename):
        '''
        @return: dictionary
        '''
        try :
            json_data=open(filename)
            data = json.load(json_data)
            json_data.close()
            return data
        except Exception as e:
            message = "Error while validating the functions file: " + filename
            logger.exception(message + str(e))
    
    def _doesFunctionExist(self,functionName, dicToUse):
        return dicToUse.has_key(functionName)
    
    def doesRemoteFunctionExist(self,functionName):
        return self._doesFunctionExist(functionName,self._functionsRemoteDic)
    
    def doesLocalFunctionExist(self,functionName):
        return self._doesFunctionExist(functionName,self._functionsLocalDic)       
    
    def getExecutableFullPath(self,functionName):
        '''
        @return: executable command corresponding to this query
        '''
        logger.debug("Looking for the executable command.")
        
        executable = self._functionsLocalDic[functionName]['executable']

        stringsToSubstitute = dict(configParser.items('General'))
        executable = executable%stringsToSubstitute
        logger.debug("Executable: %s"%executable)
        return executable
        
    def getExecutableTimeout(self,functionName):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        timeout = self._functionsLocalDic[functionName]['timeout']
        logger.debug("Executable command timeout: %d"%timeout)
        return timeout

