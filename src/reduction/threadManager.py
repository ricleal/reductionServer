#!/usr/bin/python

'''
Created on Jul 31, 2013

@author: leal

Threading module launch by the reduction server.

'''

import threading
import time
import sys
import logging
import data.dataStorage
import launcher

logger = logging.getLogger(__name__) 


    
class ThreadManager(threading.Thread):
    """
    Class it self a thread which will launch and store
    info about launched threads
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self._threadingList = []
        self._exitFlag = False
        logger.debug("Initializing Thread Manager")

    def _isThreadEntryToDelete(self,entry):
        
        if entry["thread"].isSubProcessRunning() and \
        (time.time() - entry["startTime"] > entry["timeout"]) : 
            logger.debug("Tread %s has timed out! Deleting..."%entry["variable"])
            # if time out is reason to delete we should find a safe way to kill it.
            localDataStorage = data.dataStorage.DataStorage()
            localDataStorage.updateValue(entry["variable"], 
                                                         None, "Timeout")
            return True
        if not entry["thread"].isSubProcessRunning() :
            logger.debug("Tread %s has finished! Deleting..."%entry["variable"])
            localDataStorage = data.dataStorage.DataStorage()
            localDataStorage.updateValue(entry["variable"], 
                                                         entry["thread"].output(), "Done")
            return True
        else:
            return False
            
                
    def run(self):
        """
        Check which threads are done and which have timed out
        """
        
        while True and not self._exitFlag:
            #print "Checking which threads need to be stopped:\n\t" + str(self)
            self._threadingList[:] = [x for x in self._threadingList if not self._isThreadEntryToDelete(x)]
            time.sleep(0.2)
            
    def addThread(self,variable, functionSignatureToCall,timeout=300):
        logger.debug("Launching thread: Variable: %s; Calling: %s."%(variable,functionSignatureToCall))
        
        localDataStorage = data.dataStorage.DataStorage()
        localDataStorage.addQuery(variable, functionSignatureToCall, status="querying")
        
        thisLauncher = launcher.Launcher(functionSignatureToCall,timeout)
                
        # Put threads in a list        
        startTime = time.time()
        entry = {"startTime" : startTime,
                 "variable" : variable,
                 "timeout" : timeout,
                 "thread" : thisLauncher}
        self._threadingList.append(entry)
        thisLauncher.execute()

    def removeAllThreads(self):
        '''
        Will go trought the self._threadingList and safely removes all threads
        '''
        for entry in self._threadingList:
            if entry["thread"].isSubProcessRunning() :
                entry["thread"].kill()
        
        self._threadingList = [] 
                
        

    
    def exit(self):
        logger.info("Leaving thread manager...");
        self._exitFlag = True
        
    
    def __str__(self):
        
        return str(self._threadingList)
            
            
if __name__ == '__main__':
    '''
    func1 will be removed from the list for timing out
    func2 will be removed from the list as it performed successfuly
    '''
    
    from logging import config as _config
    _config.fileConfig('../logging.ini',disable_existing_loggers=False)

    localDataStorage = data.dataStorage.DataStorage()
    import pprint

    print "Main started"
    t = ThreadManager()
    t.start()
    time.sleep(0.5)
    t.addThread("$toto","ls *.py | head -1")
    pprint.pprint(localDataStorage._data)
    time.sleep(1)
    pprint.pprint(localDataStorage._data)
    t.addThread("$tata","ls -la *.py | head -1",timeout=2)
    time.sleep(2)
    pprint.pprint(localDataStorage._data)
    t.exit()
    t.join(100) # continue but thread even if the thread is still running
    print "Main ended..."