'''
Created on Mar 13, 2014

@author: leal
'''

import storage
import config.config
import logging
from data.messages import Messages
import simplejson

logger = logging.getLogger(__name__)

class StatusHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def getQueries(self):
        logger.debug("Getting status for all queries...")
        db = storage.getDBConnection()
        res = db.getAllQueries()
        if res is None or len(res) < 1 :
            message = "The status of queries is empty. Were any queries submitted?"
            logger.error(message)
            return Messages.error(message, self.queryId);
        else:
            try:
                return simplejson.dumps(res)
            except Exception, e:
                message = "Problems while return Status json..."
                logger.exception(message  + str(e))
                return Messages.error(message, str(e));

    
    
        