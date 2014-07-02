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
    
    Class responsable for storing the available functions for each query.
    
    The specification of the queries is defined in:  
    ("General", "functions_specs_file")
    
    The file is transformed in a dictionary which is stored under the
    variable self._functionsDic
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        functionsFilename = configParser.get("General", "functions_specs_file")
        logger.debug("Using functions spec file: " + functionsFilename)
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
            message = "Error while validating the JSON of functions spec file: " + filename
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
    
    
    def getDefaultValueForParameter(self, functionName, paramName):
        '''
        If there is a 'default' key for every parameter returns its value
        Return None if there is no default defined
        '''
        try :
            params = self._functionsDic[functionName]['params']
            for p in params:
                print p
                if p['name'] == paramName:
                    return p['default']
            return None
        except Exception as e:
            message = "Error while get Default Value For Parameter=" + paramName
            logger.exception(message + str(e))
            return None
        

