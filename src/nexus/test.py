'''
Created on Jul 25, 2013

@author: leal

Unit tests for NeXus file handler

'''
import unittest
import nexusHandler


class Test(unittest.TestCase):
    
    def setUp(self):
        '''
        
        '''
        filename = '/home/leal/Documents/Mantid/IN6/157589.nxs'
        f = open(filename)
        self.nxHandler = nexusHandler.NeXusHandler(f.read())
    
    def testTitle(self):
        title = self.nxHandler.title()
        self.assertEqual(title,"Exploring the brain with neutrons")
    
    def testData(self):
        data = self.nxHandler.data()
        self.assertEqual(data.shape,(337, 1, 1024))
    
    def testDataToJson(self):
        jsonData = self.nxHandler.dataToJson()
        self.assertEqual(len(jsonData),1052982)
    
    def tearDown(self):
        del(self.nxHandler)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    unittest.main()