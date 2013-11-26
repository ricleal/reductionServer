'''
Created on Jul 22, 2013

@author: leal

Nexus handler

'''

import nxs
import logging
import simplejson
import tempfile
import os
import generalHandler

logger = logging.getLogger(__name__) 

    

class NeXusHandler(generalHandler.GeneralHandler):
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
        super(NeXusHandler, self).__init__(content)
        
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
            logger.exception("This doesn't look a valid nexus file...")
            return False
        return True
    
    def openFile(self):
        logger.debug("Opening nexus file...")
        if self.file is None:
            try:
                self.file = nxs.open(self.tempFile.name,'r')
            except  Exception:
                logger.exception("Problems opening the nexus file...It was either deleted or is not valid!")
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
                logger.exception("Problems closing the nexus file: " + str(e) )
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
    
    