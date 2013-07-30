'''
Created on Jul 29, 2013

@author: leal
'''

import numpy as np

class DummyReducer():
    '''
    Class that will old messages for interacting with the SCI sofware client
    '''


    def __init__(self,data):
        '''
        Constructor
        '''
        self.data = data
        pass
    
    def integrateThirdDimention(self):
        #data = self.data.reshape( self.data.shape[0],self.data.shape[2]);
        # data.shape : (50, 100)
        # integrate in time
        dataIntegratedInTime = np.sum(self.data,axis=1)
        return dataIntegratedInTime