'''
Created on Feb 7, 2014

@author: leal
'''

import logging
import MySQLdb
import time
from config.config import configParser

logger = logging.getLogger(__name__)

class Storage(object):
    '''
    Main data base interface
    '''


    def __init__(self):
        '''
        Constructor
        
        '''
        self.db = MySQLdb.connect(host=configParser.get("Database", "host"),
                                  user=configParser.get("Database", "user"),
                                  passwd=configParser.get("Database", "passwd"),
                                  db=configParser.get("Database", "db"))
        self.cursor = self.db.cursor()
        self.instrumentName = configParser.get("General", "instrument_name")
    
    def __del__(self):
        self.db.close()
        
    
    def insertOrUpdateNumor(self,numor,filepath):
        '''
        '''
        command = "insert into numors(numor,instrument_name,filepath,update_date) values(%d,'%s','%s','%s')\
        on duplicate key update filepath='%s', update_date='%s'"%(numor,self.instrumentName,filepath,self.__now(),
                                filepath,self.__now())
        logger.debug("Query: " + command)
        try:
            self.cursor.execute(command)
            self.db.commit()
        except MySQLdb.Error, e:
            try:
                logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                logger.error("MySQL Error: %s" % str(e))
    
    def insertQuery(self,queryId,numorList):
        '''
        '''
        command = "insert into queries(query_id,instrument_name,update_date) values('%s','%s','%s')"%(queryId,self.instrumentName,self.__now())
        logger.debug("Query: " + command)
        try:
            self.cursor.execute(command)
            if len(numorList) <=0 :
                self.db.rollback()
            else: 
                for numor in numorList:
                    command = "insert into queries_has_numors(query_id,numor,instrument_name) values('%s',%d,'%s')"%(queryId,numor,self.instrumentName)
                    logger.debug("Query: " + command)
                    self.cursor.execute(command)
                self.db.commit()
        except MySQLdb.Error, e:
            try:
                logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                logger.error("MySQL Error: %s" % str(e))
            self.db.rollback();       
    
    def getListOfValidNumors(self):
        command = "select numor from numors where instrument_name = '%s'"% self.instrumentName
        logger.debug("Query: " + command)
        ret = [];
        try:
            self.cursor.execute(command)
            for i in range(self.cursor.rowcount):
                row = self.cursor.fetchone()
                ret.append(row[0])
        
        except MySQLdb.Error, e:
            try:
                logger.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                logger.error("MySQL Error: %s" % str(e))
        return ret
    
            
    def __now(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    
def main():
    db = Storage()
    db.insertOrUpdateNumor(1234, "/tmp/1234_1");
    db.insertOrUpdateNumor(1234, "/tmp/1234_2");
    db.insertOrUpdateNumor(1234, "/tmp/1234_3");
    db.insertOrUpdateNumor(1235, "/tmp/1235_1");
    
    import uuid
    # this fails
    db.insertQuery(uuid.uuid4(),[123,124])
    db.insertQuery(uuid.uuid4(),[1234])
    db.insertQuery(uuid.uuid4(),[1234,1235])
    
    rows = db.getListOfValidNumors()
    print rows
    
if __name__ == "__main__":
    main()
        