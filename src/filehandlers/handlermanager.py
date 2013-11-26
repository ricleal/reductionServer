'''
Created on Nov 22, 2013

@author: leal
'''

import nexusHandler
import asciiHandler

class Manager(object):
    '''
    This class will check the stream content.
    Validate the content and return the corresponding file handler.
    '''

    registeredHandlers = [nexusHandler.NeXusHandler,
                          asciiHandler.AsciiHandler]

    def __init__(self, content):
        '''
        Constructor
        
        @param content : stream received by http
        '''
        self.content = content
    
    def getRespectiveHandler(self):
        """
        According to the content, it will return the rigth handler 
        """
        ret = None;
        for h in self.registeredHandlers :
            thisHandler = h(self.content)
            if thisHandler.isValid() :
                ret = thisHandler
                break
        return ret
    
                
        
        
        
    
    
        