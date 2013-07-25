'''
Created on Jul 25, 2013

@author: leal
'''
import unittest
import handler


class Test(unittest.TestCase):

    def testNexusReader(self):
        filename = "/home/leal/Documents/Mantid/IN6/157589.nxs"
        try:
            nxHandler = handler.Handler(filename)
            print "Title read from the Nexus file:", nxHandler.title()
        except  Exception as e:
            print "Problems opening the nexus file: ", e
            raise

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    unittest.main()