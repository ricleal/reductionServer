'''
Created on Jul 22, 2013

@author: leal
'''

import nxs


class Handler:
    '''
    Handler to deal with a nexus file
    Keeps a pointer for the open file
    
    '''
    def __init__(self, filename):
        print "Opening nexus file:", filename
        try:
            self.file = nxs.open(filename,'r')
        except  Exception as e:
            print "Problems opening the nexus file: ", e
            raise
        
    def title(self):
        self.file.opengroup('entry0')
        self.file.opendata('title')
        title =  self.file.getdata()
        self.file.closedata()
        self.file.closegroup()
        return title
    
    def __del__(self):
        print "Closing nexus file..."
        try:
            self.file.close()
        except  Exception as e:
            print "Problems closing the nexus file: ", e
            raise     

    