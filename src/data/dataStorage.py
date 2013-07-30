'''
Created on Jul 30, 2013

@author: leal
'''

class DataStorage():
    '''
    Class to store data for a file being threated
    Valid per file (numor id)
    '''


    def __init__(self,numor):
        '''
        Constructor
        '''
        self._data = {"numor":numor}
        
    
    def addQuery(self, variable, value, desc):
        '''
        Add query to the database
        For query of type:
        {$toto : cell}
        variable = $toto 
        value = cell
        desc = 'Unit cell'
        '''
        self._data[variable]={"value": None, "query" : value , "desc" : desc}
    
    def updateValue(self, variable, value):
        '''
        Add the result from reduction query to the data
        For query of type:
        {$toto : [10 10 10 90 90 90]}
        variable = $toto 
        value = [10 10 10 90 90 90]
        '''
        self._data[variable]["value"]=value
    
    def getValue(self,variable):
        return self._data[variable]["value"]
    
    def __str__(self):
        return str(self._data)

def main():
    d = DataStorage('11214')
    d.addQuery('$toto', 'cell', 'Unit cell')
    # Do processing
    d.updateValue('$toto', [10, 10, 10, 90, 90 ,90])
    print "get value:" , d.getValue('$toto') 
    print d
    
if __name__ == "__main__":
    main()
        
        