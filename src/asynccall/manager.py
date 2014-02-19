'''
Created on Feb 18, 2014

@author: leal
'''

from pythonlauncher import PythonScriptLauncher
from shelllauncher import ShellLauncher



class LaunchManager(object):
    '''
    classdocs
    '''

    def __init__(self, launcherNameToUse):
        '''
        Constructor
        
        @param content : stream received by http
        '''
        self.classLauncher = locals()[launcherNameToUse]
    
    def initLauncher(self,executableCommand):
        self.launcher =  self.classLauncher(executableCommand)
        
    
    def sendCommand(self,command,timeout):
        self.launcher.sendCommand(command,timeout)
    
    
    