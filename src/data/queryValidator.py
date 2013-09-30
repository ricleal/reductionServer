'''
Created on Sep 19, 2013

@author: leal
'''

import logging
from config.config import configParser
from data.dataStorage import dataStorage

import data.messages

logger = logging.getLogger(__name__) 

class QueryValidator(object):
    '''
    classdocs
    
    @todo: 
    
    '''


    def __init__(self,query):
        '''
        Constructor
        '''
        self._query = query
        functionsDicFilename = configParser.get("General", "functions_specs_file")
        self._functionsDic = self._importJsonFromFile(functionsDicFilename)
        self._thisFunction = None
    
    def _importJsonFromFile(self,filename):
        import json
        json_data=open(filename)
        data = json.load(json_data)
        json_data.close()
        return data
        
    def validateFunction(self):
        '''
        @todo:Validate query agains schema
        @return: None if it's valid otherwise error message
        '''        
        try: 
            self._thisFunction = self._functionsDic[self._query["function"]]
        except Exception as e:
            message = "Error while validating the query function. Is it a valid function?"
            logger.exception(message)
            return data.messages.Messages.error(message,{ "exception_message" : str(e), "valid_functions" : self._functionsDic.keys() } )
        
        return None
    
    def validateNumors(self):
        # See if numors exist first in the data storage
        from data.dataStorage import dataStorage
        numorsToProcess = set(self._query["input_params"]["numors"])
        allNumors = set(dataStorage.keys())
        if not numorsToProcess.issubset(allNumors) :
            logger.error("Numors don't exist in the database: " +  str(list(numorsToProcess - allNumors)))
            return data.messages.Messages.error("Numors do not exist in the database",{"invalid_numors":list(numorsToProcess - allNumors)})    
        return None
        
    
    def getExecutable(self):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        logger.debug("Looking for the executable command.")
        
        executable = self._thisFunction['local_mapping']['executable']
#         In [134]: dict(config.items('General'))
#         Out[134]: 
#         {'instrument_name': 'IN5',
#          'scripts_folder': '/home/leal/git/reductionServer/scripts'}

        stringsToSubstitute = dict(configParser.items('General'))
        executable = executable%stringsToSubstitute
        logger.debug("Executable: %s"%executable)
        
        # Check input parameters:
        
        inputParamsAsStr = " "        
        inputParams = self._query["input_params"]
        for i in inputParams.keys():
            if i == "numors":
                for j in inputParams["numors"]:
                    inputParamsAsStr+=dataStorage[j].filename()+ " "
        
        executable = executable + inputParamsAsStr
        
        logger.debug("Executable: %s"%executable)
        return executable
        
    def getExecutableTimeout(self):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        timeout = self._thisFunction["timeout"]
        logger.debug("Executable command timeout: %d"%timeout)
        return timeout

if __name__ == '__main__':
    import ast
    query = """{
    "function":"theta_vs_counts",
    "input_params":{
        "numors":[
            12345
        ]
        
    }
}"""
    contentAsDict = ast.literal_eval(query)
    queryValidator = QueryValidator(contentAsDict)
    queryValidator.validate()
    queryValidator.getExecutable()
        
    
    
        