'''
Created on Oct 29, 2013

@author: leal


This is a test and is not connected to the main code.
The idea is to have 2 capped collections: one for numors another for queries.
When numors reach the limits it should delete the temporary files it points to.
To date MongoDB does not implement triggers and there's no way to delete the files when a item is dropped.



'''
from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

from config.config import configParser 

class Database(object):
    '''
    Generic class to access MongoDB.
    
    Uses / create a database accordinf to instrument name
    '''
    
    db = None
    collections={}
    
    def __init__(self,databaseNamePrefix='reduction'):
        '''
        Constructor
        '''
        self.client = MongoClient() # localhost
        
        databasename =  databaseNamePrefix + configParser.get("General", "instrument_name")
        self.db = self.client[databasename]
        logger.debug("Using database: %s."%databasename)
    
    def createCollection(self, name, max=22, size=10240, capped=True):
        """
        Create a collection.
        @param name:
        @param max:
        @param size:
        @param capped:
        """
        try:
            self.collections[name] = self.db.create_collection( name=name, size=size, capped=capped,max=max ) 
            logger.debug("Collection %s created."%name)
        except:
            # Assuming it becauase name in self.db.collection_names()
            logger.info("Collection %s already exist. Skipping creation..."%name)
            self.collections = self.db[name]
                        

#     def _init(self):
#         # TODO : change constants to globals!
#         try :
#             self.numors = self.db.create_collection( name="numors", size=10240, capped=True,max=22 )
#             logger.debug("Collection numors created.")
#         except:
#             self.numors = self.db.numors
#             logger.info("Collection already exist. Skipping creation...")
#             
#         try:
#             self.queries = self.db.create_collection( name="queries", size=10240, capped=True,max=128 )
#             logger.debug("Collection queries created.")
#         except:
#             self.queries = self.db.queries
#             logger.info("Collection already exist. Skipping creation...")
        
        
    def dumpCollectionToArray(self,collectionName,constraint={}):
        """
        
        @param collectionName: name
        @param constraint: constraing for collection.find()
        """
        #from bson.json_util import dumps
        #return dumps(cursor)
        cursor =  self.collections[collectionName].find(constraint);
        return [i for i in cursor]
        
    
#     def findFilePath(self,numors):
#         """
#         Return a list of files for given numors
#         @param numors: list of numors
#         """
#         cursor = self.numors.find({"numor":  { "$in": numors}})
#         return [i['filename'] for i in cursor]

#     def storeFile(self,filepath):
#         """
#         
#         @param filepath:
#         """
#         import gridfs
#         try :
#             self.fsCollection = self.db.create_collection( name="fsCollection", size=10240, capped=True,max=2 )
#             logger.debug("fsCollection created.")
#         except:
#             self.fsCollection = self.db.fsCollection
#             logger.info("fsCollection already exist. Skipping creation...")
#         fs = gridfs.GridFS(database=self.db,collection='fsCollection')
#         with fs.new_file( filename='/tmp/file.txt', 
#                           content_type='text/plain', 
#                           my_other_attribute=42) as fp:
#             fp.write('New file')
#         print fp._id
#         
#         
#         # overwrite
#         with fs.new_file(filename='/tmp/file.txt', content_type='text/plain') as fp:
#             fp.write('Overwrite the so-called "New file"')
#         
#         print fp._id
#         gridFile = fs.get_last_version('/tmp/file.txt')
#         print gridFile.read()
#         print gridFile.filename
#         print gridFile.aliases
#         gridFile.close()
# 
#         return fp._id
        


    def __del__(self):
        self.client.close()
    
    def dropDatabase(self):
        """
        Never use this one :)
        """
        self.db.drop()


if __name__ == '__main__':
    db = Database()
    db.createCollection('numors')
    db.createCollection('queries')
    
    
    for i in range(1000,1020):
        db.collections['numors'].insert({"numor": i, "filename": "/tmp/file_%d.nxs"%i})
    
    db.collections['queries'].insert({"query_id" : "001","numor": [1000,1001,1002]})
    objectId = db.collections['queries'].insert({"query_id" : "002","numor": [1004,1005,1006]})
    # modifify
    db.collections['queries'].save({ "_id": objectId, "query_id" : "002","numor": [1004,1005,1007]})
    import pprint
    pprint.pprint(db.dumpCollectionToArray('queries'))
    pprint.pprint(db.dumpCollectionToArray('numors'))
# /    pprint.pprint(db.findFilePath([1012,1015]))
    
    
    
    
    

