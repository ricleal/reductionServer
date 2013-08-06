'''
Created on Jul 30, 2013

@author: leal
'''
import simplejson
import threading

class DataStorage():
    '''
    Class to store data for a file being threated
    Valid per file (numor id)
    '''

    def __init__(self,numor=None):
        '''
        Constructor
        '''
        # Lock
        self.lock = threading.Lock()
        with self.lock:
            self._data = {}
            if numor is not None:
                self._data = {"numor":numor}
    
    def data(self):
        with self.lock:
            return self._data
    def empty(self):
        with self.lock:
            return len(self._data) <= 0
        
    def __str__(self):
        with self.lock:
            return str(self._data)
    
    
    def addQuery(self, variable, value, status, desc=None):
        '''
        Add query to the database
        For query of type:
        {$toto : cell}
        variable = $toto 
        value = cell
        desc = 'Unit cell'
        '''
        with self.lock:
            self._data[variable]={"value": None, "query" : value , "desc" : desc,
                                  "status": status}
    
    def updateValue(self, variable, value, status):
        '''
        Add the result from reduction query to the data
        For query of type:
        {$toto : [10 10 10 90 90 90]}
        variable = $toto 
        value = [10 10 10 90 90 90]
        '''
        with self.lock:
            self._data[variable]["value"]=value
#             try: # to make sure when a a value is assigned there's no error field
#                 del  self._data[variable]["error"]
#             except KeyError:
#                 pass
            self._data[variable]["status"]=status
            
    def updateValueWithStatus(self, variable, message):
        with self.lock:
            self._data[variable]["status"]=message
    
    def getValue(self,variable):
        with self.lock:
            return self._data[variable]["value"]
    def getNumor(self):
        with self.lock:
            return self._data["numor"]
    
    def toJson(self):
        with self.lock:
            return simplejson.dumps(self._data)
    


def main():
    d = DataStorage()
    print d
    if d._data == {}:
        print "D is empty!"
    
    
    print "---------------------"
    d = DataStorage('11214')
    d.addQuery('$toto', 'cell', 'Unit cell')
    # Do processing
    d.updateValue('$toto', [10, 10, 10, 90, 90 ,90], "processing")
    print d
    d.updateValueWithStatus('$toto', "timeout")
    print d
    print "get value:" , d.getValue('$toto') 
    print d
    
if __name__ == "__main__":
    main()
        
        