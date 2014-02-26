#!/usr/bin/python

'''
Created on Feb 26, 2014

@author: leal
'''
import unittest
from unittest import TestSuite


def load_tests(loader, tests, pattern):
    '''
    Run all tests in the current directory starting by 
    '''

    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('.', pattern='test*.py'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite

if __name__ == '__main__':
    unittest.main()