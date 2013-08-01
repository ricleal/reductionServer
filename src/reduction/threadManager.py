#!/usr/bin/python

'''
Created on Jul 31, 2013

@author: leal
'''

import threading
import time
import sys
import logging

logger = logging.getLogger(__name__) 

# dummy functions called from the TreadableFunctionCaller
def func1():
    func_name = sys._getframe().f_code.co_name
    print "Calling:", func_name
    time.sleep(5)
    return "ret func1"

def func2(par):
    func_name = sys._getframe().f_code.co_name
    print "Calling:", func_name, "with parameter:", par
    time.sleep(1)
    return "ret func2"

class TreadableFunctionCaller(threading.Thread):
    """
    Test class to be threaded
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
        print "* Thread func started:", self.name
        # Using eval is evil, but let's use it here:
        self.result = eval(self.name)
        print "* Thread func done   :", self.name
        print self.result


    
class ThreadManager(threading.Thread):
    """
    Class it self a thread wich will launch and store
    info about launched threads
    """
    def __init__(self,timeout):
        threading.Thread.__init__(self)
        self._threadingList = []
        self._exitFlag = False
        self._timeOut = timeout # seconds

    def _isThreadEntryToDelete(self,entry):
        if entry["thread"].isAlive() and \
        (time.time() - entry["startTime"] > self._timeOut) or \
        not entry["thread"].isAlive() :
            print "Tread %s to delete"%entry["thread"].name
            # if time out is reason to delete we should find a safe way to kill it.
            return True
        else:
            return False
            
                
    def run(self):
        while True and not self._exitFlag:
            #print "Checking which threads need to be stopped:\n\t" + str(self)
            self._threadingList[:] = [x for x in self._threadingList if not self._isThreadEntryToDelete(x)]
            time.sleep(0.2)
            
    def addThread(self,functionSignatureToCall):
        print "Launching thread: ", functionSignatureToCall
        t = TreadableFunctionCaller(functionSignatureToCall);
        # Put threads in a list        
        startTime = time.time()
        entry = {"startTime" : startTime,
                 "thread" : t}
        self._threadingList.append(entry)
        t.start()


    
    def exit(self):
        print "Exiting! Threads still running:" + str(self) 
        self._exitFlag = True
    
    def __str__(self):
        
        return str(self._threadingList)
            
            
if __name__ == '__main__':
    '''
    func1 will be removed from the list for timing out
    func2 will be removed from the list as it performed successfuly
    '''
    print "Main started"
    t = ThreadManager(timeout=4)
    t.start()
    time.sleep(0.5)
    t.addThread("func1()")
    time.sleep(1)
    t.addThread("func2('param1')")
    time.sleep(5)
    t.exit()
    t.join(100) # continue but thread even if the thread is still running
    print "Main ended..."