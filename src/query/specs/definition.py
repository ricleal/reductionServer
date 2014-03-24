'''
Created on Feb 24, 2014

@author: leal
'''

import logging
from config.config import configParser
import json

logger = logging.getLogger(__name__) 

class QuerySpecs(object):
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
        functionsFilename = configParser.get("General", "functions_specs_file")
        self._functionsDic = self._importJsonFromFile(functionsFilename)
        
    
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
    
    def doesFunctionExist(self,functionName):
        return self._functionsDic.has_key(functionName)
    
    def getExecutableFullPath(self,functionName):
        '''
        @return: executable command corresponding to this query
        '''
        logger.debug("Looking for the executable command.")
        
        executable = self._functionsDic[functionName]['executable']

        stringsToSubstitute = dict(configParser.items('General'))
        executable = executable%stringsToSubstitute
        logger.debug("Executable: %s"%executable)
        return executable
        
    def getExecutableTimeout(self,functionName):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        try :
            timeout = self._functionsDic[functionName]['timeout']
            logger.debug("Executable command timeout: %d"%timeout)
            return timeout
        except:
            return None

