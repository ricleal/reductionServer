'''
Created on Jul 22, 2013

@author: leal

ascii content

'''


import logging
import os
from content.handler.filename import File

logger = logging.getLogger(__name__) 

    

class Ascii(File):
    '''
    asciiHandler to deal with a ascii file
    Keeps a pointer for the open file
    
    Only handles one file at the time.
    
    '''
    
    def __init__(self, content):
        '''
        @param content: binary stream - contents of the ascii file 
        '''    
        logger.debug("Creating Ascii Handler")
        super(Ascii, self).__init__(content,suffix=".txt")
        
    def isValid(self):
        """
        Is this a valid ILL ASCII File
        """
        try :
            self.openFile()
            header = "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR";
            firstLine = self.file.readline();
            if firstLine.find(header) >= 0:
                self.closeFile()
                return True;
            else:
                logger.debug("Does not look an Ascii valid file. Deleting temporary file: %s" % self.tempFile.name)
                try :
                    os.remove(self.tempFile.name)
                except  Exception as e:
                    logger.error("Error removing temporary file: " + str(e))
                return False
        except Exception, e:
            logger.exception("Problems validating the ascii file: " + str(e) )
            logger.debug("Deleting temporary file: %s" % self.tempFile.name)
            try :
                os.remove(self.tempFile.name)
            except  Exception as e:
                logger.error("Error removing temporary file: " + str(e))
            return False
    
    def openFile(self):
        logger.debug("Opening ascii file...")
        if self.file is None:
            try:
                self.file = open(self.tempFile.name,'r')
            except  Exception as e:
                logger.exception("Problems opening the ascii file: " + str(e) )
                raise
        else:
            logger.warning("Ascii file appears to be open already.")
            
    def closeFile(self):
        logger.debug("Closing ascii file...")
        if self.file is not None:
            try:
                self.file.close()
                self.file = None
            except  Exception as e:
                logger.exception("Problems closing the ascii file: " + str(e) )
                raise
        else:
            logger.warning("Ascii file appears to be closed already.")
        

if __name__ == '__main__':
    pass
    
    