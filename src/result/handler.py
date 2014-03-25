'''
Created on Mar 13, 2014

@author: leal
'''

import storage
import config.config
import logging
from data.messages import Messages
import simplejson
import zlib

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
            try:
                return simplejson.dumps(res[0])
            except Exception, e:
                message = "Problems validating json results for query id %s..."%self.queryId
                logger.exception(message  + str(e))
                return Messages.error(message, str(e));

    def getQueryZipped(self):
        logger.debug("Getting results zipped for query id = " + self.queryId)
        db = storage.getDBConnection()
        res = db.getQuery(self.queryId)
        if len(res) != 1 :
            message = "Zipped result for query id %s is multiple (len = %d)!!!"%(self.queryId,len(res))
            logger.error(message)
            return Messages.error(message, self.queryId);
        else:
            try:
                logger.debug("Zipping results for query id = " + self.queryId)
                jsonContent = simplejson.dumps(res[0])
                logger.debug("Original content size: %d"%len(jsonContent))
                jsonContentZipped = zlib.compress(jsonContent)
                logger.debug("Zipped content size: %d"%len(jsonContentZipped)) 
                return jsonContentZipped
            except Exception, e:
                message = "Problems validating json results for zipped query id %s."%self.queryId
                logger.exception(message  + str(e))
                return Messages.error(message, str(e));

    
        