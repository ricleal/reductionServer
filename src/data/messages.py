'''
Created on Sep 27, 2013

@author: leal

Default JSON MESSAGES

'''
import ast
import logging
import config.config

logger = logging.getLogger(__name__) 

class Messages(object):
    '''
    classdocs
    '''
    
    messageTemplate = """{
        'success' : '%r',
        'message' : '%s',
        'details' : %r
    }"""
        
    
    @staticmethod
    def success(message,details=''):
        messageAsStr = Messages.messageTemplate%(True,message,details)
        logger.debug(messageAsStr)
        messageAsDic = ast.literal_eval(messageAsStr)
        return messageAsDic    
    
    @staticmethod
    def error(message,details=''):
        messageAsStr = Messages.messageTemplate%(False,message,details)
        logger.debug(messageAsStr)
        messageAsDic = ast.literal_eval(messageAsStr)
        return messageAsDic
    
    @staticmethod
    def errorDetailed(message,complementaryMessage,value):
        details = """{
        'message' : %r, 
        'value' : %r
        }"""%(complementaryMessage,value)
        messageAsStr = Messages.messageTemplate%(False,message,
                                                 ast.literal_eval(details))
        logger.debug(messageAsStr)
        messageAsDic = ast.literal_eval(messageAsStr)
        return messageAsDic


if __name__ == '__main__':
    Messages.success("OK")
    Messages.success("OK", "File received")
    Messages.error("Error")
    Messages.error("Error",details='There was an error processing XPTO.')
    Messages.error("Error adding X.",details={'error' : 'xpto', 'valid' : [1,2,3]})
    Messages.errorDetailed("Error adding X.","Valid values are", [1,2,3,5])
    
        