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
import collections

logger = logging.getLogger(__name__) 


class NexusStorage(object):
    '''
    Class to store the nexus file
    Identified by the numor.
    
    Borg singleton config object
    '''
    __shared_state = {}
    _data = collections.deque(maxlen=22)
    
    def __init__(self):
        
        #implement the borg pattern (_shared_state)
        self.__dict__ = self.__shared_state
    
    def __numorExistsInData(self,numor):
        for idx, value in enumerate(self._data) :
            if numor == value.numor():
                return idx
        return None
    
    def __str__(self):
        res = ""
        for idx, value in enumerate(self._data) :
            res += "%s -> %s, "%(idx,value.numor())
        return res
    
    def insert(self,numor,content):
        
        tmpNxHandler = NeXusHandler(numor, content)
        
        idx = self.__numorExistsInData(numor)
        
        if idx is not None:
            self._data[idx] = tmpNxHandler
        else:
            self._data.appendleft(tmpNxHandler)
        
    
    def fileNameLastInserted(self):
        return self._data[0].filename()
    
    def fileName(self,numor):
        for value in self._data :
            if numor == value.numor():
                return value.filename()
        return None
    def size(self):
        return len(self._data)
    

class NeXusHandler(object):
    '''
    NeXusHandler to deal with a nexus file
    Keeps a pointer for the open file
    
    Only handles one file at the time.
    
    '''
    
    def __init__(self, numor, content):
        '''
        @param content: binary stream - contents of the nexus file 
        '''
        
        logger.debug("Parsing request...")
        
        self.__numor = numor
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False)
        self.tempFile.write(content)
        self.tempFile.close()
        
        self.__openNexusFile()

    def __del__(self):
        logger.debug("Deleting NeXus temporary file: %s"%self.tempFile.name)

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
    
    def numor(self):
        return self.__numor
    
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
        jsonData = simplejson.dumps(data.tolist())
        return jsonData
    

    