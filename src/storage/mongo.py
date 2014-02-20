'''
Created on Feb 14, 2014

@author: leal
'''

from pymongo import MongoClient

import datetime

import logging
logger = logging.getLogger(__name__)


class MongoDB(object):
    '''
    classdocs
    '''
    
    db = None

    def __init__(self,uri,instrumentName):
        '''
        Constructor
        '''
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()
        self.instrumentName = instrumentName
    
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

