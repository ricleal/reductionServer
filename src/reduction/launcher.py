#!/usr/bin/python

'''
Created on Aug 9, 2013

@author: leal

Launcher to run shell commands.



'''
import subprocess
import threading
import time


class Launcher(threading.Thread):
    '''
    Launcher class.
    Constructer gets the shell command as parameter.
    
    '''

    def __init__(self,command,timeout):
        '''
        Constructor
        @param command: Shell commands
        @param timeout: Timeout
         
        '''
        
        threading.Thread.__init__(self)
        self.__command = command
        self.__timeout = timeout
        
        self.__out = None
        self.__err = None
        self.__process = None
        self.__startTime = None
    
    def run(self):
        '''
        Communicate  blocks until the command is fully executed
        Executed through a thread
        '''
        
        self.__startTime = time.time()

        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__out, self.__err = self.__process.communicate()
    
    def execute(self):
        self.start()
    
    def wait(self):
        '''
        either wait for the process to finish
        or for the timeout
        '''
        elapsedTime =  time.time() - self.__startTime
        timeout = self.__timeout - elapsedTime 
        if timeout >0:
            self.join(self.__timeout)
        # if after the timeout it is still alive
        if self.is_alive():
            self.__process.terminate()
            self.join()
    
    def executeAndWait(self):
        '''
        Blocks until process executes or times out
        '''
        self.start()
        self.join(self.__timeout)
        # if after the timeout it is still alive
        if self.is_alive():
            self.__process.terminate()
            self.join()
    
    def isSubProcessRunning(self):
        if self.__process.poll() is None:
            return True
        else:
            return False
    
    def exit(self):
        self.__process.terminate()
        self.join()
            
    def error(self):
        return self.__err
    
    def output(self):
        return self.__out
    def returnCode(self):
        return self.__process.returncode
    

if __name__ == "__main__":
    
    # short command
    l = Launcher('ls -la',2)
    l.executeAndWait()
    print "** Error:",
    print l.error()
    print "** Out:",
    print l.output()
    print "** Return Code:",
    print l.returnCode()
    
    # long command with shor timeout
    # waits to be done
    print "******************************"
    l = Launcher('sleep 10',1)
    l.executeAndWait()
    print "** Time out run out: Return Code =/= 0:",
    print l.returnCode()
    
    # shor command long time out
    # Launchs command and don't hangup
    print "******************************"
    l = Launcher('sleep 2',5)
    l.execute()
    print "I'm doing other stuff"
    time.sleep(1)
    print "Is subprocess running?",
    print l.isSubProcessRunning()
    time.sleep(2)
    print "Should be done. Return Code must be zero if it's done:",
    print l.returnCode()
    
    