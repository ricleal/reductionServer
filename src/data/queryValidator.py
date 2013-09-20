'''
Created on Sep 19, 2013

@author: leal
'''

import logging

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
    
    def validate(self):
        '''
        @todo: 
        Validate query agains schema
        @return: None if it's valid otherwise error message
        '''
        logger.debug("Validating query")
    
    def getExecutable(self):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        logger.debug("Looking for the executable command")
        return "ls -l"
        
    def getExecutableTimeout(self):
        '''
        @todo: 
        @return: executable command corresponding to this query
        '''
        logger.debug("Looking for the executable command timeout")
        return 10
        
    
    
        