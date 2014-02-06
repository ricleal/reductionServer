'''
Created on Jul 25, 2013

@author: leal

Unit tests for NeXus file handler

'''
import unittest
import nexusHandler
import logging
import config.config

logger = logging.getLogger(__name__) 

class Test(unittest.TestCase):
    
    def setUp(self):
        '''
        Run BEFORE every single test!
        '''
        filename = '/home/leal/Documents/Mantid/IN6/157589.nxs'
        self.f = open(filename).read()
        self.nxHandler = nexusHandler.NeXusHandler(self.f)
    
    def testTitle(self):
        self.nxHandler.openFile()
        title = self.nxHandler.title()
        self.assertEqual(title,"Exploring the brain with neutrons")
    
    def testData(self):
        self.nxHandler.openFile()
        data = self.nxHandler.data()
        self.assertEqual(data.shape,(337, 1, 1024))
    
    def testDataToJson(self):
        self.nxHandler.openFile()
        jsonData = self.nxHandler.dataToJson()
        self.assertEqual(len(jsonData),1052982)
    
    def testFilename(self):
        filename = self.nxHandler.filename()
        print 'filename:',filename
        self.assertTrue(filename.startswith('/tmp'))
    
    def testIsValid(self):
        valid = self.nxHandler.isValid()
        print 'Valid:',valid
        self.assertTrue(valid)
    
    def tearDown(self):
        del(self.nxHandler)
        

if __name__ == "__main__":
    # To run a single test: python -m unittest testnexus.Test.testIsValid
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
#    unittest.main()