'''
Created on Jul 25, 2013

@author: leal

Dummy set of tests

'''
import unittest
import dummyReducer
import numpy as np
import simplejson

class Test(unittest.TestCase):
    
    def setUp(self,data=None):
        '''
        
        '''
        if data is None:
            self.dummyData = np.arange(5000,dtype='int32').reshape((50,100))
        else:
            self.dummyData = data
        
        self.dummyAxisX = range(1,len(self.dummyData)+1)
        self.reducer = dummyReducer.DummyReducer(self.dummyData)
        
        
    def testIntegration(self):
        # 3D to 2D
        # data.shape : (50, 1, 100)
        data = self.reducer.integrateThirdDimention()
        
        ret = {"axis_x" : {"label" : "Dummy X label",
                           "data" : self.dummyAxisX },
               "axis_y" : {"label" : "Dummy Y label",
                           "data" : data.tolist() }
               }
        jsonData = simplejson.dumps(ret)
        expectedJsonResult = '{"axis_x": {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], "label": "Dummy X label"}, "axis_y": {"data": [4950, 14950, 24950, 34950, 44950, 54950, 64950, 74950, 84950, 94950, 104950, 114950, 124950, 134950, 144950, 154950, 164950, 174950, 184950, 194950, 204950, 214950, 224950, 234950, 244950, 254950, 264950, 274950, 284950, 294950, 304950, 314950, 324950, 334950, 344950, 354950, 364950, 374950, 384950, 394950, 404950, 414950, 424950, 434950, 444950, 454950, 464950, 474950, 484950, 494950], "label": "Dummy Y label"}}'
        self.assertEqual(jsonData,expectedJsonResult)

    
    

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    unittest.main()