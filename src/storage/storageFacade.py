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

    def getListOfAllNumors(self):
        # This returns an array like:
        # [{u'numor': 1000}, {u'numor': 1001}, ... ,{u'numor': 1234}]
        arr = self.db.dumpCollectionToArray("numors",{},{'numor':True,'_id':False})
        return [i['numor'] for i in arr]
        
    
    
