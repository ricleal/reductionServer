'''
Created on Mar 13, 2014

@author: leal
'''

import storage
import config.config
import logging
from data.messages import Messages

logger = logging.getLogger(__name__)

class HandlerResult(object):
    '''
    classdocs
    '''


    def __init__(self, queryId):
        '''
        Constructor
        '''
        self.queryId = queryId
    
    def getQuery(self):
        logger.debug("Getting results for query id = " + self.queryId)
        db = storage.getDBConnection()
        res = db.getQuery(self.queryId)
        if len(res) != 1 :
            message = "Result for query id %s is multiple (len = %d)!!!"%(self.queryId,len(res))
            logger.error(message)
            return Messages.error(message, self.queryId);
        else:
            return res[0]

    
    
        