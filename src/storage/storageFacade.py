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
    
    
    def insertQuery(self,queryDefinitionInJson):
        self.db.insert('queries',queryDefinitionInJson)
        
    def updateQuery(self,queryId, queryJson):
        self.db.update('queries',{"queryId" : queryId } , queryJson)


    def getListOfAllNumors(self):
        # This returns an array like:
        # [{u'numor': 1000}, {u'numor': 1001}, ... ,{u'numor': 1234}]
        arr = self.db.dumpCollectionToArray("numors",{},{'numor':True,'_id':False})
        return [i['numor'] for i in arr]
        
    
    def getListOfFiles(self,numors):
        # This returns an array like:
        # [{u'numor': 1000}, {u'numor': 1001}, ... ,{u'numor': 1234}]
        arr = self.db.dumpCollectionToArray("numors",{"numor" : { "$in" : numors } },{'filename':True,'_id':False})
        return [i['filename'] for i in arr]
    
    
