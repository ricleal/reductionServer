'''
Created on Jul 22, 2013

@author: leal
'''

import nxs
import logging
import simplejson


logger = logging.getLogger(__name__) 

class NeXusHandler:
    '''
    NeXusHandler to deal with a nexus file
    Keeps a pointer for the open file
    
    '''
    def __init__(self, filename):
        logger.debug("Opening nexus file: " + filename)
        try:
            self.file = nxs.open(filename,'r')
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
    
    def __del__(self):
        logger.debug("Closing nexus file...")
        try:
            self.file.close()
        except  Exception as e:
            logger.error( "Problems closing the nexus file: " +str(e) )
            raise     

    