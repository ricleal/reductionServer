'''
Created on Feb 17, 2014

@author: leal
'''

from storage.mongo import MongoDB

from config.config import configParser

import logging
logger = logging.getLogger(__name__)


class StorageFacade(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        dataBaseName = configParser.get("Database", "name")
        dataBaseUri = configParser.get("Database", "uri")
        instrumentName = configParser.get("General", "instrument_name")
        
        self.db = globals()[dataBaseName](dataBaseUri,instrumentName)
    
    
    def insertOrUpdateNumor(self,numor,filename):
        self.db.insertOrUpdate('numors', numor, {"filename": filename } )
    
    
    def insertQuery(self,queryId,numorList):
        self.db.insert('queries',{"id": queryId, "numors" : numorList})


    
    
