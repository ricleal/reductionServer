'''
Created on Feb 24, 2014

@author: leal
'''
import unittest

from handlers.validator.file import FileValidator

class Test(unittest.TestCase):

    nexusFile = '/home/leal/Documents/Mantid/IN5/095762.nxs'
    textFile = '/home/leal/Documents/Mantid/D20/858939'
    url = '/home/leal/Documents/Mantid/D20/858939'

    def testValidatorNexus(self):
        content = open(self.nexusFile)
        v = FileValidator(content.read())
        message = v.validateFile(1234)
        content.close()
        self.assertDictContainsSubset({'success' : 'True','details' : 'The handlers is: NeXus'}, message)

    def testValidatorText(self):
        content = open(self.textFile)
        v = FileValidator(content.read())
        message = v.validateFile(1234)
        content.close()
        self.assertDictContainsSubset({'success' : 'True','details' : 'The handlers is: Ascii'}, message)

    def testValidatorURL(self):
        content = self.url
        v = FileValidator(content)
        message = v.validateFile(1234)
        self.assertDictContainsSubset({'success' : 'True','details' : 'The handlers is: Url'}, message)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testValidatorNexus']
    unittest.main()