#!/usr/bin/python

'''
Created on Jul 25, 2013

@author: leal

Unit tests will be in this file

'''
import unittest
import reductionServer
import pycurl
import cStringIO
from multiprocessing import Process
import time
import os

queryId = None

class TestServer(unittest.TestCase):
    """
    Unit test for server
    2 class methods setUpClass and tearDownClass are invoked before and
    after all tests to start and stop the server respectivelly. 
    
    """
    
    @classmethod
    def setUpClass(self):
        '''
        Start the server
        '''
        self.p = Process(target=reductionServer.main, args=(None,))
        self.p.start()
        time.sleep(0.1)
        #p.join()
        self.url = "http://localhost:8080"
        self.filename = '/home/leal/Documents/Mantid/IN6/157589.nxs'
        
    def test_a_Alive(self):
        '''
        curl -v http://localhost:8080/
        '''
        
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.POST,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '')
        buf.close()
    
    def postFile(self,numor):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/file/%d"%numor)
        c.setopt(c.POST,1)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/octet-stream'])
        filesize = os.path.getsize(self.filename)
        c.setopt(pycurl.POSTFIELDSIZE, filesize)
        fin = open(self.filename, 'rb')
        c.setopt(pycurl.READFUNCTION, fin.read)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        buf.close()
        return ret
    
    def test_b_File(self):
        '''
        cd ~/Documents/Mantid/IN6
        curl -v -X POST --data-binary @157589.nxs http://localhost:8080/file/157589
        '''
        ret = self.postFile(1)
        self.assertEqual(ret, '{"success": "OK"}')
        
        ret = self.postFile(2)
        self.assertEqual(ret, '{"success": "OK"}')
        
          
    def test_c_Query(self):
        '''
        curl -v -H "Content-Type: application/json" \
         -H "Accept: application/json"  \
         -X POST \
         -d '{"query":"sofw","numors":[1,2]}' \
         http://localhost:8080/query
        '''
        
        textToPost = """{"query":"sofw","numors":[1,2]}"""
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/query")
        c.setopt(c.POST,1)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        c.setopt(pycurl.HTTPHEADER, ['Numor: 1234'])
        
        c.setopt(c.POSTFIELDS, textToPost)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        global queryId
        queryId = eval(ret)['query_id']
        self.assertEqual(ret, """{"query_id": "%s"}"""%queryId )
        buf.close()
        

    def test_d_Results(self):
        '''
        curl -v -X POST http://localhost:8080/results/QUERY_ID
        '''
        time.sleep(2)
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        global queryId
        c.setopt(c.URL, self.url+"/results/" + queryId)
        c.setopt(c.POST,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertTrue('"status": "done"' in ret)
        buf.close()

    @classmethod
    def tearDownClass(self):
        '''
        Kill the server
        '''
        time.sleep(1)
        self.p.terminate()
        # to make sure everything finished (i.e. thread manager)!
        time.sleep(1)
         
#         import signal
#         print self.p, self.p.is_alive()
#         print "Exit code = SIGTERM?", self.p.exitcode == -signal.SIGTERM
#     


if __name__ == "__main__":
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestServer)
    #unittest.TextTestRunner(verbosity=2).run(suite)

     
