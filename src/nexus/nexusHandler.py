'''
Created on Jul 22, 2013

@author: leal
'''

import nxs
import logging
import simplejson
import tempfile
import os

logger = logging.getLogger(__name__) 

class NeXusHandler:
    '''
    NeXusHandler to deal with a nexus file
    Keeps a pointer for the open file
    
    '''
    
    def __init__(self, content):

        logger.debug("Parsing request...")
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False)
        self.tempFile.write(content)
        self.tempFile.close()
        
        self.__openNexusFile()

    def __del__(self):
        logger.debug("Deleting NeXus temporary file...")

        try :
            os.remove(self.tempFile.name)
        except  Exception as e:
            logger.error("Error removing temporary nexus file: " + str(e))
        
    
    def __openNexusFile(self):
        logger.debug("Opening nexus file...")
        try:
            self.file = nxs.open(self.tempFile.name,'r')
        except  Exception as e:
            logger.error("Problems opening the nexus file: " + str(e) )
            raise
        
    def title(self):
        self.file.opengroup('entry0')
        self.file.opendata('title')
        title =  self.file.getdata()
        self.file.closedata()
        self.file.closegroup()
        return title
    
    def data(self):
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
        jsonData = simplejson.dumps(data.tolist())
        return jsonData
    

    