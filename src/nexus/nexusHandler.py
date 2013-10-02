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

logger = logging.getLogger(__name__) 

    

class NeXusHandler(object):
    '''
    NeXusHandler to deal with a nexus file
    Keeps a pointer for the open file
    
    Only handles one file at the time.
    
    '''
    
    def __init__(self, content):
        '''
        @param content: binary stream - contents of the nexus file 
        '''
        
        logger.debug("Parsing request...")
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False, prefix='live_', suffix='.nxs')
        self.tempFile.write(content)
        self.tempFile.close()
        
        self.file = None

    def __del__(self):
        logger.debug("Deleting NeXus temporary file: %s"%self.tempFile.name)

        try :
            os.remove(self.tempFile.name)
        except  Exception as e:
            logger.error("Error removing temporary nexus file: " + str(e))
        
    
    def openFile(self):
        logger.debug("Opening nexus file...")
        if self.file is None:
            try:
                self.file = nxs.open(self.tempFile.name,'r')
            except  Exception as e:
                logger.exception("Problems opening the nexus file: " + str(e) )
                raise
        else:
            logger.warning("Nexus file appears to be open already.")
            
    def closeFile(self):
        logger.debug("closing nexus file...")
        if self.file is not None:
            try:
                file.close()
                self.file = None
            except  Exception as e:
                logger.exception("Problems closing the nexus file: " + str(e) )
                raise
        else:
            logger.warning("Nexus file appears to be closed already.")
        
    def filename(self):
        return self.tempFile.name
    
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
    
    def __repr__(self, *args, **kwargs):
        return self.filename()

if __name__ == '__main__':
    pass
    
    