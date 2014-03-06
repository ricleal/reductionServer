'''
Created on Nov 22, 2013

@author: leal
'''

from content.handler.nexus import NeXus
from content.handler.ascii import Ascii
from content.handler.url import Url

class Manager(object):
    '''
    This class will check the stream content.
    Validate the content and return the corresponding file content.
    '''

    registeredHandlers = [NeXus, Ascii, Url]

    def __init__(self, content):
        '''
        Constructor
        
        @param content : stream received by http
        '''
        self.content = content
    
    def getRespectiveHandler(self):
        """
        According to the content, it will return the rigth content 
        """
        ret = None;
        for h in self.registeredHandlers :
            thisHandler = h(self.content)
            if thisHandler.isValid() :
                ret = thisHandler
                break
        return ret
    
                
        
        
        
    
    
        