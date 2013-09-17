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
        from logging import config as _config
        _config.fileConfig('../logging.ini',disable_existing_loggers=False)
        
        filename = '/home/leal/Documents/Mantid/IN6/157589.nxs'
        self.f = open(filename).read()
        self.nxHandler = nexusHandler.NeXusHandler(self.f)
    
    def testTitle(self):
        title = self.nxHandler.title()
        self.assertEqual(title,"Exploring the brain with neutrons")
    
    def testData(self):
        data = self.nxHandler.data()
        self.assertEqual(data.shape,(337, 1, 1024))
    
    def testDataToJson(self):
        jsonData = self.nxHandler.dataToJson()
        self.assertEqual(len(jsonData),1052982)
    
    def testFilename(self):
        filename = self.nxHandler.filename()
        print 'filename:',filename
        self.assertTrue(filename.startswith('/tmp'))
    

    
    def tearDown(self):
        del(self.nxHandler)
        

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)