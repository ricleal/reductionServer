'''
Created on Sep 23, 2013

@author: leal
'''

import logging
import numpy as np
from helper.config import config

import sys
sys.path.append(config.get('General','mantid.home'))

from mantid.simpleapi import *

logger = logging.getLogger(__name__) 

class MantidSimple(object):
    def __init__(self,filename):
        self.inputWorkspaceName = "in"
        self.outputWorkspaceName = "out"
        self.wsRaw = Load(Filename=filename,OutputWorkspace=self.inputWorkspaceName)
        self.wsIntegrated = None
        
    def rawDataXAxis(self):
        return self.wsRaw.extractX() # 2D copy of workspace data
    
    def rawDataValues(self):
        return self.wsRaw.extractY() # 2D copy of workspace data
    
        
    def _integration(self):
        if self.wsIntegrated == None :
            self.wsIntegrated = Integration(InputWorkspace=self.inputWorkspaceName,
                                            OutputWorkspace=self.outputWorkspaceName)
    
    def integratedXAxis(self):
        self._integration()
        return self.wsIntegrated.extractX() # 2D copy of workspace data
    
    def integratedValues(self):
        self._integration()
        return self.wsIntegrated.extractY() # 2D copy of workspace data
        
        
if __name__ == '__main__':
    testfile = r'/home/leal/Documents/Mantid/IN6/157589.nxs'
    m = MantidSimple(testfile)
    
    print m.rawDataXAxis()[0]
    
    print m.integratedXAxis()[0]
    
    print np.transpose(m.integratedValues())
    
    