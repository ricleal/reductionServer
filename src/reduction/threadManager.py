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

logger = logging.getLogger(__name__) 



# dummy functions called from the TreadableFunctionCaller
def func1():
    func_name = sys._getframe().f_code.co_name
    time.sleep(1)
    return "ret func1"

def func2(par=None):
    func_name = sys._getframe().f_code.co_name
    time.sleep(5)
    return "ret func2"

class TreadableFunctionCaller(threading.Thread):
    """
    Class to be threaded
    This class will call the reduction functions
    """
    def __init__(self,functionSignatureCall):
        """
        name will be an existing function with parameter list, e.g.:
        "fullName( name = 'Joe', family = 'Brand' )"
        
        """
        threading.Thread.__init__(self,name=functionSignatureCall)
        self.result = None

    def run(self):
        ''' Function to be threaded '''
        logger.debug("Calling %s within a thread..."%self.name) 
        # Using eval is evil, but let's use it here:
        try :
            # TODO:
            # I'm trusting that what comes in functionSignatureCall
            # can be called with eval
            # This must be though in the future
            self.result = eval(self.name)
            logger.debug("Function %s successfully evaluated!"%self.name)
        except Exception as e:
            logger.error("Error while evaluating %s : %s" % (self.name,str(e)))
            self.result = None
        


    
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
        
        if entry["thread"].isAlive() and \
        (time.time() - entry["startTime"] > entry["timeout"]) : 
            logger.debug("Tread %s has timed out! Deleting..."%entry["variable"])
            # if time out is reason to delete we should find a safe way to kill it.
            localDataStorage = data.dataStorage.DataStorage()
            localDataStorage.updateValue(entry["variable"], 
                                                         None, "Timeout")
            return True
        if not entry["thread"].isAlive() :
            logger.debug("Tread %s has finished! Deleting..."%entry["variable"])
            localDataStorage = data.dataStorage.DataStorage()
            localDataStorage.updateValue(entry["variable"], 
                                                         entry["thread"].result, "Done")
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
        
        
        t = TreadableFunctionCaller(functionSignatureToCall);
        # Put threads in a list        
        startTime = time.time()
        entry = {"startTime" : startTime,
                 "variable" : variable,
                 "timeout" : timeout,
                 "thread" : t}
        self._threadingList.append(entry)
        t.start()

    def removeAllThreads(self):
        '''
        Will go trought the self._threadingList and safely removes all threads
        '''
        for t in self._threadingList:
            if ["thread"].isAlive() :
                #TODO
                # safely kill it
                pass
        
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

    print "Main started"
    t = ThreadManager()
    t.start()
    time.sleep(0.5)
    t.addThread("$toto","func1()")
    time.sleep(1)
    t.addThread("$tata","func2('param1')",timeout=2)
    time.sleep(5)
    t.exit()
    t.join(100) # continue but thread even if the thread is still running
    print "Main ended..."