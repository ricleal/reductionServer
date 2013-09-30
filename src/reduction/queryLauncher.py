#!/usr/bin/python

'''
Created on Jul 31, 2013

@author: leal

Threading module launch by the reduction server.

'''

import threading
import time
import logging
import helper.launcher
import data.messages

logger = logging.getLogger(__name__) 
    
class QueryLauncher():
    """
    Launchs and stores info in QueryStorage about launched processes.
    
    """

    def __init__(self):
        '''
        '''
        from data.queryStorage import queryStorage
        self._queryStorage = queryStorage
        self.lastThread = None
    
    def processQuery(self, queryId):
        self.lastThread = threading.Thread(target=self._launchQueryInBackground, args=(queryId,))
        self.lastThread.start()
                
    
    def _launchQueryInBackground(self, queryId):
        
        logger.debug("Launching the query in background...")
        
        self._queryStorage[queryId]["start_time"] = time.time()
        self._queryStorage[queryId]["start_local_time"] = time.asctime(time.localtime(time.time()))
        self._queryStorage[queryId]["status"] = "running" 
        
        # TODO mapping name and local command and timeout
        # fill in time out etc
        commandToExecute = self._queryStorage[queryId]["executable"]
        timeout = self._queryStorage[queryId]["timeout"]
        
        l = helper.launcher.Launcher(commandToExecute, timeout)    
        self._queryStorage[queryId]["launcher"] = l 
        l.launch() # Blocks until executed or error
        
                # get the output as json
        try:
            import ast
            self._queryStorage[queryId]["output"] = ast.literal_eval(l.output())
        except Exception, e:
            message = "JSON of the output processing file looks invalid: " + str(e)
            logger.exception(message)
            logger.debug(l.output())
            self._queryStorage[queryId]["output"] = data.messages.Messages.error(message,str(e))
        
        self._queryStorage[queryId]["status"] = "done" 
        self._queryStorage[queryId]["return_code"] = l.returnCode()
        self._queryStorage[queryId]["end_time"] = time.time()
        self._queryStorage[queryId]["end_local_time"] = time.asctime(time.localtime(time.time()))
        self._queryStorage[queryId]["error"] = l.error()


    
    


    def killAllRunningLaunchers(self):
        
        for k in self._queryStorage.keys():
            if self._queryStorage[k]["launcher"].isSubProcessRunning() :
                self._queryStorage[k]["launcher"].kill()
            
        

                
            
            
if __name__ == '__main__':
    '''

    '''
    
    from logging import config as _config
    _config.fileConfig('../logging.ini', disable_existing_loggers=False)

    import pprint
    
    from data.queryStorage import queryStorage
    
        
    e = {'query' : "call_xpto", 'params':[1,2,4], "executable" : "ls /tmp"}
    import uuid
    queryId = str(uuid.uuid4())
    queryStorage[queryId] = e
    print len(queryStorage),queryStorage

    q = QueryLauncher()
    q.processQuery(queryId)    
    
    pprint.pprint(queryStorage[queryId])
    q.lastThread.join()
    #time.sleep(0.3) # wait for launcher to finish
    pprint.pprint(queryStorage[queryId])
    
    
    print "Main ended..."
