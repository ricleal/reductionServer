'''

@author: leal

URL content

content is url type:

scheme://domain:port/path?query_string#fragment_id


This content won validade the file for now!
It only ckeck if it exists!

'''


import logging
import os
from urlparse import urlparse
from content.handler.filename import Handler

logger = logging.getLogger(__name__) 

    

class Url(Handler):
    '''
    asciiHandler to deal with a ascii file
    Keeps a pointer for the open file
    
    Only handles one file at the time.
    
    '''
    
    def __init__(self, content):
        '''
        @param content: binary stream - contents of the ascii file 
        '''    
        logger.debug("Creating URL Handler")
         
        # remove new line
        self.content = content.rstrip()
        
        # Not using the super constructor as I don't expect a file
        # super(Url, self).__init__(content)
        
        self.parsedUrl = None
        
    def isValid(self):
        """
        Is this a valid url and the path exists?
        """

        try :
            self.parsedUrl = urlparse(self.content);
            #logger.debug("File path: " + self.filepath)
        except Exception, e:
            logger.exception("Problems validating the ascii file: " + str(e) )
            return False
        
        if not os.path.exists(self.parsedUrl.path) :
            logger.error("File " + self.parsedUrl.path + " does not exist.")
            return  False
        else:
            return True
    
    def filename(self):
        return self.parsedUrl.path
        

if __name__ == '__main__':
    pass
    
    