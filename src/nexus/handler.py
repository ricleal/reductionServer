'''
Created on Jul 22, 2013

@author: leal
'''

import nxs
import logging

logger = logging.getLogger(__name__) 

class Handler:
    '''
    Handler to deal with a nexus file
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
    
    def __del__(self):
        logger.debug("Closing nexus file...")
        try:
            self.file.close()
        except  Exception as e:
            logger.error( "Problems closing the nexus file: " +str(e) )
            raise     

    