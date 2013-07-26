'''
Created on Jul 23, 2013

@author: leal
'''

import handler_sm

import tempfile
import os

import logging
logger = logging.getLogger(__name__) 


class Handler:
    def __init__(self):
        
        logger.info("Initialising SM Handler...")
        self._fsm = handler_sm.Handler_sm(self)
        self._fsm.setDebugFlag(True)
        self.nxHandler = None
        self._satus = {}
        self._results = {} # dictionary with queries and results
        # Start from the first state
        self._fsm.enterStartState()
        
    
    def sm(self):
        return self._fsm
    
    def _formatStatus(self, message, status="OK"):
        logger.debug("Setting status to: " + status + " -> " + message)
        self._satus['status'] = status
        self._satus['message'] = message
    
    def setStatus(self,message):
        self._formatStatus(message)
    
    def setErrorStatus(self,message):
        self._formatStatus(message, 'KO')
    
    def setSuccessStatus(self,message):
        self._formatStatus(message)
    
    def status(self):
        return self._satus
    
    def results(self):
        return self._results
    
    def processFile(self, request):
        logger.debug("Parsing request...")
        
        content = request.body.read()
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False)
        self.tempFile.write(content)
        self.tempFile.close()
      
        try :
            import nexus.handler as nx
            self.nxHandler = nx.Handler(self.tempFile.name)  
            logger.info("* Title read from the Nexus file: " + self.nxHandler.title())
            # Do whatever needed with the nexus file
            
        except  Exception as e:
            self.nxHandler = None
            logger.error("Error while reading the nexus file: " + str(e))
            
        
    def cleanUp(self):
        logger.debug("Cleaning up!")
        try :
            del(self.nxHandler)
        except  Exception as e:
            logger.error("Error deleting nexus handler: " + str(e))
            
        try :
            os.remove(self.tempFile.name)
        except  Exception as e:
            logger.error("Error removing temporary nexus file: " + str(e))
        
    
    def checkFileProcessing(self):
        logger.debug("Checking if NeXus file was well processed...")
        if self.nxHandler is None:
            self._fsm.failure()
        else:
            self._fsm.success()
    
    def handleQuery(self,content):
        '''
        content if of type:
        { "$toto" : [10,10,10,90,90,90], "$tata" : 178, "$titi" : [0, 0, 0] }
        
        '''
        # merge dictionaries
        for k,v in content.iteritems():
            print k,v
        
        # do some processing
        
        
        self._results = reduce(lambda x,y: dict(x, **y), (self._results, content))
        
    def handleResult(self,content):
        '''
        Receives a list of variables and stores the result
        '''
        for i in content:
            self._results[i]
        
        
            
        
    

    