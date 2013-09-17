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



    
class QueryManager():
    """
    Launchs and stores info about launched processes
    
    """

    def __init__(self):
        '''
        '''
        from data.queryStorage import queryStorage
        self._queryStorage = queryStorage
    
    
    def processQuery(self, queryId):
        t = threading.Thread(target=self.launchQueryInBackground, args=(queryId,))
        t.start()
                
    
    def launchQueryInBackground(self, queryId):
        
        self._queryStorage[queryId]["start_time"] = time.time()
        self._queryStorage[queryId]["start_local_time"] = time.asctime(time.localtime(time.time()))
        self._queryStorage[queryId]["status"] = "running" 
        
        # TODO mapping name and local command and timeout
        # fill in time out etc
        query = self._queryStorage[queryId]["query"]
        commandToExecute = "ls /home"
        timeout = 10
        
        l = launcher.Launcher(commandToExecute, timeout)    
        self._queryStorage[queryId]["launcher"] = l 
        l.launch()
        
        # # Blocks until executed or error
        self._queryStorage[queryId]["status"] = "done" 
        self._queryStorage[queryId]["return_code"] = l.returnCode()
        self._queryStorage[queryId]["end_time"] = time.time()
        self._queryStorage[queryId]["end_local_time"] = time.asctime(time.localtime(time.time()))
        self._queryStorage[queryId]["error"] = l.error()
        self._queryStorage[queryId]["output"] = l.output()
    
    


    def killAllRunningLaunchers(self, entry):
        
        for k in self._queryStorage.keys():
            if self._queryStorage[k]["launcher"].isSubProcessRunning() :
                self._queryStorage[k]["launcher"].kill()
            
        

                
            
            
if __name__ == '__main__':
    '''
    func1 will be removed from the list for timing out
    func2 will be removed from the list as it performed successfuly
    '''
    
    from logging import config as _config
    _config.fileConfig('../logging.ini', disable_existing_loggers=False)

    from data.queryStorage import queryStorage
    for i in range(10):
        qTxt = "xpto_%d"%i
        e = {'query' : qTxt, 'params':[i]*5}
        import uuid
        id = str(uuid.uuid4())
        queryStorage[id] = e
        print len(queryStorage),queryStorage
    
    q = QueryManager()
    q.processQuery(id)
    time.sleep(0.3)
    queryStorage[id]["launcher"]
    
    print queryStorage
    print "Main ended..."
