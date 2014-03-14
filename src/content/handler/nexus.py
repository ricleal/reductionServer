'''
Created on Jul 22, 2013

@author: leal

Nexus content

'''

import nxs
import logging
import simplejson
import os

from content.handler.filename import File


logger = logging.getLogger(__name__) 

    

class NeXus(File):
    '''
    NeXusHandler to deal with a nexus file
    Keeps a pointer for the open file
    
    Only handles one file at the time.
    
    '''
    
    def __init__(self, content):
        '''
        @param content: binary stream - contents of the nexus file 
        '''    
        logger.debug("Creating Nexus Handler")
        super(NeXus, self).__init__(content,suffix=".nxs")
        
    def isValid(self):
        """
        Is this a valid Nexus file?
        """
        try :
#             fp = nxs.open(self.tempFile.name,'r')
#             fp.close()
            self.openFile();
            self.closeFile();
        except Exception:
            logger.info("This doesn't look a valid nexus file...")
            logger.debug("Deleting temporary file: %s" % self.tempFile.name)
            try :
                os.remove(self.tempFile.name)
            except  Exception as e:
                logger.error("Error removing temporary file: " + str(e))
            return False
        return True
    
    def openFile(self):
        logger.debug("Opening nexus file...")
        if self.file is None:
            try:
                self.file = nxs.open(self.tempFile.name,'r')
            except  Exception:
                logger.info("Problems opening the nexus file...It was either deleted or is not valid!")
                raise
        else:
            logger.warning("Nexus file appears to be open already.")
            
    def closeFile(self):
        logger.debug("closing nexus file...")
        if self.file is not None:
            try:
                self.file.close()
                self.file = None
            except  Exception as e:
                logger.info("Problems closing the nexus file: " + str(e) )
                raise
        else:
            logger.warning("Nexus file appears to be closed already.")
        
    
    def title(self):
        self.file.opengroup('entry0')
        self.file.opendata('title')
        title =  self.file.getdata()
        self.file.closedata()
        self.file.closegroup()
        return title
    
    def data(self):
        '''
        gets the data field
        TODO:
        Needs to be modified in order to cleverly
        find the data field (e.g. that with signal=1,
        or the biggest array in the file)   
        '''
        self.file.opengroup('entry0')
        self.file.opengroup('data')
        self.file.opendata('data')
        data = self.file.getdata()
        self.file.closedata()
        self.file.closegroup()
        self.file.closegroup()
        return data
    
    def dataToJson(self):
        data = self.data()
        jsonData = simplejson.dumps(self.data().tolist())
        return jsonData
    

if __name__ == '__main__':
    pass
    
    