'''
Created on Feb 12, 2014

@author: leal
'''

from data.messages import Messages 

import json
import logging

logger = logging.getLogger(__name__) 

class Json(object):
    '''
    classdocs
    '''


    def __init__(self,rawContent):
        '''
        Constructor
        '''
        self.rawContent = rawContent
        self.jsonContent = None
        
    
    def validate(self):
        
        try :
            self.jsonContent = json.loads(self.rawContent)
            return self.jsonContent
        except Exception, e:
            self.jsonContent = None
            message = "JSON appears to be invalid."
            logger.exception(message  + str(e))
            return None