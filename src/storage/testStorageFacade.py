'''
Created on Feb 20, 2014

@author: leal
'''
import unittest

import storage

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDatabase(self):
        db = storage.getDBConnection()
        for i in range(1000,1003):
            db.insertOrUpdateNumor(i,"/tmp/file_%d.nxs"%i)
        for i in range(1000,1003):
            db.insertOrUpdateNumor(i,"/tmp/file_%d.nxs"%(i+10))
    
        for i in range(1000,1003):
            db.insertQuery({"queryId" : i*10, "numors" : [1000,1001] , "timeout":30})
        
        l = db.getListOfAllNumors()
        print l
        for i in range(1000,1003) :
            self.assertIn(i, l)
        
        l = db.getListOfFiles([1000, 1001, 1002, 44235, 1234])
        print l
        self.assertIn('/tmp/file_1010.nxs', l)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMongo']
    unittest.main()