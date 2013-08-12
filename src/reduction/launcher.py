#!/usr/bin/python

'''
Created on Aug 9, 2013

@author: leal

Launcher to run shell commands.

'''
import subprocess

class Launcher(object):
    '''
    Launcher class.
    Constructer gets the shell command as parameter.
    
    '''


    def __init__(self,command):
        '''
        Constructor
        '''
        self.__command = command
        self.__out = None
        self.__err = None
        self.__process = None
    
    def execute(self):
        '''
        blocks until the command is executed
        '''
        
        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__out, self.__err = self.__process.communicate()
        
    def error(self):
        return self.__err
    
    def output(self):
        return self.__out
    def returnCode(self):
        return self.__process.returncode
    

if __name__ == "__main__":
    
    shellCommand = 'ls -la'
    l = Launcher(shellCommand)
    l.execute()
    print "** Error:"
    print l.error()
    print "** Out:"
    print l.output()
    print l.returnCode()
    