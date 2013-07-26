'''
Created on Jul 25, 2013

@author: leal
'''
import unittest
import reductionServer
import pycurl
import cStringIO
from multiprocessing import Process
import time
import os

class Test(unittest.TestCase):
    
    def setUp(self):
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
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.POST,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '{"status": "Yes I am up and running!"}')
        buf.close()
        
    def testStatus(self):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/status")
        c.setopt(c.POST,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '{"status": "OK", "message": "Idle"}')
        buf.close()
    
    def testFile(self):
        '''
        cd ~/Documents/Mantid/IN6
        curl -v -X POST --data-binary @157589.nxs http://localhost:8080/file
        '''
        
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url+"/file")
        c.setopt(c.POST,1)
        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/octet-stream'])
        filesize = os.path.getsize(self.filename)
        c.setopt(pycurl.POSTFIELDSIZE, filesize)
        fin = open(self.filename, 'rb')
        c.setopt(pycurl.READFUNCTION, fin.read)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        ret = buf.getvalue()
        self.assertEqual(ret, '{"status": "OK", "message": "Waiting for queries"}' )
        buf.close()

    def tearDown(self):
        '''
        Kill the server
        '''
        self.p.terminate()
    


if __name__ == "__main__":
    unittest.main()