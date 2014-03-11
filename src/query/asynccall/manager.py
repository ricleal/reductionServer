'''
Created on Feb 18, 2014

@author: leal
'''

## This needs to be here!!!
## Only use the import in the config.ini file
from query.asynccall.pythonlauncher import PythonScriptLauncher
from query.asynccall.shelllauncher import ShellLauncher

import ast


from config.config import configParser

def getClass( className, argsToConstructor=None ):
    '''
    returns a class instance given a name
    :param className : class name 
    :type className : str
    
    '''
    if argsToConstructor is None:
        return globals()[className]()    
    else:
        return globals()[className](argsToConstructor)



class LaunchManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        
        @param launcherNameToUse : Parameters of the launcher
        '''
        
        classLauncher = globals()[configParser.get("Launcher", "name")]
        executable = configParser.get("Launcher", "executable")
        if executable is not None and len(executable.strip())>0:
            classLauncherInitParams = ast.literal_eval(executable)
            self.launcher = classLauncher(classLauncherInitParams)
        else:
            self.launcher = classLauncher()
               
    
    def sendCommand(self,command,timeout):
        self.launcher.sendCommand(command,timeout)
    
    
    def getResult(self):
        '''
        Python:
        After the script run, dump workspace to json and then to a tmp file. Return a cat tmpfile
        Lamp:
        1 . create a tmp file in python and send commando to lamp:  export_json,s,file="${temp_filename}"
        2. Correct the tmp file - python script
        3. Return a cat tmpfile
        
        @return: JSON
        '''
        pass
    