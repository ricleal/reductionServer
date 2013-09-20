'''
Created on Jul 30, 2013

@author: leal
'''

import logging
import helper.dict

logger = logging.getLogger(__name__) 

class DataStorage(helper.dict.LimitedSizeDict):
    '''
    Class to store data
    
    
    Table for Nexus + numor
    {
    numor:
    nexus_handler :
    }
    
    '''
    
#     def __new__(cls, *args, **kwargs):
#         '''
#         Singleton
#         '''
#         if not hasattr(cls, '_instance'):
#             cls._instance = dict.__new__(cls, *args, **kwargs)
#         return cls._instance
#     
#     def __init__(self, *args, **kwds):
#         '''
#         Constructor
#         As it's a singleton if self.size_limit exists alredy 
#         does not call the super.__init__
#         '''
#         try:
#             self.size_limit
#         except:
#             helper.dict.LimitedSizeDict.__init__(self, *args, **kwds)
    
    def __init__(self, *args, **kwds):
        '''
        Constructor
        '''
        helper.dict.LimitedSizeDict.__init__(self, *args, **kwds)
        
    def isValidNumor(self,numor):
        return numor in self
    
    def findInvalidNumors(self,numors):
        '''
        Return non existent numors from the input param
        '''
        res = []
        for n in numors:
            if not self.isValidNumor(n) :
                res.append(n)
        return res
    
    def deleteContent(self):
        for k in self.keys():
            del self[k]

            
dataStorage = DataStorage(size_limit=22)

def main():
    q = DataStorage(size_limit=5)
    
    for i in range(10):
        e = "Nexus File content %d"%i
        q[i] = e
        print len(q),q
    print q.isValidNumor(7)
    print q.isValidNumor(12)
    
    print q.findInvalidNumors([1,2,7,8])
    
    q2 = DataStorage()
    for i in range(10,20):
        e = "Nexus File content %d"%i
        q2[i] = e
        print len(q2),q2
    
    
if __name__ == "__main__":
    main()
        
        
