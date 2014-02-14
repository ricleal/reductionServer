'''
Created on Feb 14, 2014

@author: leal
'''

from pymongo import MongoClient
from config.config import configParser
import datetime

import logging
logger = logging.getLogger(__name__)


class MongoDB(object):
    '''
    classdocs
    '''
    
    db = None

    def __init__(self):
        '''
        Constructor
        '''
        self.client = MongoClient(configParser.get("Database", "uri"))
        self.db = self.client.get_default_database()
        
        self.instrumentName = configParser.get("General", "instrument_name")
    
    def insertOrUpdate(self,collectionName,numor,dataInDicFormat):
        data = dataInDicFormat
        data['numor']= numor
        data['last_updated_date']= self.__now()
        data['instrument_name']= self.instrumentName
        self.db[collectionName].update({'numor' : numor}, data, upsert=True );
    
    def insert(self,collectionName,dataInDicFormat):
        data = dataInDicFormat
        data['last_updated_date']= self.__now()
        data['instrument_name']= self.instrumentName
        self.db[collectionName].insert(data);
    
    def dumpCollectionToArray(self,collectionName,constraint={}):
        """    
        @param collectionName: name
        @param constraint: constraing for collection.find()
        """
        cursor =  self.db[collectionName].find(constraint);
        return [i for i in cursor]
    
    def __now(self):
        return datetime.datetime.now()

    
def test():
    db = MongoDB()
    for i in range(1000,1003):
        db.insertOrUpdate('numors', i, {"filename": "/tmp/file_%d.nxs"%i} )

    for i in range(1000,1003):
        db.insertOrUpdate('numors', i, {"filename": "/tmp/file_%d.nxs"%(i+10)} )

    for i in range(1000,1003):
        db.insert('queries',{"id": i*10})
    
    print db.dumpCollectionToArray('numors',{'numor': 1000})
   
if __name__ == "__main__":
    test()       