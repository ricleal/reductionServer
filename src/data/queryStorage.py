'''
Created on Sep 16, 2013

@author: leal
'''


import logging
import helper.dict

logger = logging.getLogger(__name__) 

class QueryStorage(helper.dict.LimitedSizeDict):
    '''
    Class to store data for a file being threated
    
    
    Table for Queries:
    {
    queries : {
        numors: 
        query :
        uuid :
        start_time:
        end_time : 
        timeout :
        result : {
            
            }
        }
    }
       
    '''
    
    
#     def __new__(cls, *args, **kwargs):
#         '''
#         Singleton
#         '''
#         if not hasattr(cls, '_instance'):
#             cls._instance = dict.__new__(cls, *args, **kwargs)
#             print "Create instance..."
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
    
    def addQuery(self,queryId,query):
        self[queryId]=query
        
    

queryStorage = QueryStorage(size_limit=256)
        
def main():
    
    for i in range(10):
        qTxt = "xpto_%d"%i
        e = {'query' : qTxt, 'params':[i]*5}
        import uuid
        id = str(uuid.uuid4())
        queryStorage[id] = e
        print len(queryStorage),queryStorage
    
    
    print
    print len(queryStorage),queryStorage
    
    queryStorage.addQuery('232323-23-232-323-1212', {"query":"sofw"})
    print len(queryStorage),queryStorage
    
    
if __name__ == "__main__":
    main()