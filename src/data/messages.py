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
        'success' : '%(success)r',
        'general_message' : '%(general_message)s',
        'errors' : %(errors)r
    }"""
    
        
    @staticmethod
    def success(message):
        data = {'success': True, 'general_message': message, "errors" : ''}
        messageAsStr = Messages.messageTemplate%data
        logger.debug(messageAsStr)
        messageAsDic = ast.literal_eval(messageAsStr)
        return messageAsDic
    
    
    @staticmethod
    def error(message,errors):
        data = {'success': False, 'general_message': message, "errors" : errors}
        messageAsStr = Messages.messageTemplate%data
        logger.debug(messageAsStr)
        messageAsDic = ast.literal_eval(messageAsStr)
        return messageAsDic

if __name__ == '__main__':
    Messages.success("message")
    Messages.success("This a message")
    Messages.error("Error", {'code' : 1234})
    
    
        