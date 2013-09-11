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
    
    def testAlive(self):
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
          
    def testFile(self):
        '''
        cd ~/Documents/Mantid/IN6
        curl -v -H "Numor: 1234" -X POST --data-binary @157589.nxs http://localhost:8080/file
        '''
        
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/file")
        c.setopt(c.POST,1)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/octet-stream'])
        c.setopt(pycurl.HTTPHEADER, ['Numor: 1234'])
        filesize = os.path.getsize(self.filename)
        c.setopt(pycurl.POSTFIELDSIZE, filesize)
        fin = open(self.filename, 'rb')
        c.setopt(pycurl.READFUNCTION, fin.read)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '{"numor": "1234"}')
        buf.close()
          
    def testQuery(self):
        '''
        curl -v -H "Content-Type: application/json" \
        -H "Numor: 1234" \
         -H "Accept: application/json"  \
         -X POST \
         -d '{"$toto":"/home/leal/git/reductionServer/bin/test1.sh", "$tata":"/home/leal/git/reductionServer/bin/test1.sh /bin/sh"}' \
         http://localhost:8080/query
        '''
        
        textToPost = """{"$toto":"/home/leal/git/reductionServer/bin/test1.sh", "$tata":"/home/leal/git/reductionServer/bin/test1.sh /bin/sh"}"""
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
        self.assertEqual(ret, '{"$toto": {"status": "querying", "query": "/home/leal/git/reductionServer/bin/test1.sh", "value": null, "desc": null}, "numor": "1234", ' +
                         '"$tata": {"status": "querying", "query": "/home/leal/git/reductionServer/bin/test1.sh /bin/sh", "value": null, "desc": null}}')
        buf.close()

    def testResults(self):
        '''
        curl -v -X POST http://localhost:8080/results
        '''
        time.sleep(2)
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/results")
        c.setopt(c.POST,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '{"$toto": {"status": "Done", "query": "/home/leal/git/reductionServer/bin/test1.sh", "value": "Usage: /home/leal/git/reductionServer/bin/test1.sh filename\\n", "desc": null}, "numor": "1234", ' + 
                         '"$tata": {"status": "Done", "query": "/home/leal/git/reductionServer/bin/test1.sh /bin/sh", "value": "File found\\n", "desc": null}}')
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

     
