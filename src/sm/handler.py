'''
Created on Jul 23, 2013

@author: leal
'''

import handler_sm

import tempfile
import os


class Handler:
    def __init__(self):
        print "Initialising SM Handler..."
        self._fsm = handler_sm.Handler_sm(self)
        self._fsm.setDebugFlag(True)
        self.nxHandler = None
        self._satus = {}
        
        self._fsm.enterStartState()
        
    
    def sm(self):
        return self._fsm
    
    def _formatStatus(self, message, status="OK"):
        print "Setting status to: ", status, " -> ", message
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
        
    
    def processFile(self, request):
        print "Parsing data:", request
        
        content = request.body.read()
    
        # Need to write the file on disk! there's no open stream in nexus library for python
        self.tempFile = tempfile.NamedTemporaryFile(delete=False)
        self.tempFile.write(content)
        self.tempFile.close()
      
        try :
            import nexus.handler as nx
            self.nxHandler = nx.Handler(self.tempFile.name)  
            print "* Title read from the Nexus file:", self.nxHandler.title()
            #self.setSuccessStatus("Nexus file well parsed.")
            
            
        except  Exception as e:
            print "Error while reading the nexus file:", e
            #self.setErrorStatus("Nexus file parsing failed:  "+ str(e) )
        
        
    def cleanUp(self):
        try :
            del(self.nxHandler)
        except  Exception as e:
            print "Error:", e
            
        try :
            os.remove(self.tempFile.name)
        except  Exception as e:
            print "Error removing temporary nexus file:", e
        
    
    def checkFileProcessing(self):
        print "** checkFileProcessing"
        if self.nxHandler is None:
            self._fsm.failure()
        else:
            self._fsm.success()
    
    def notify(self):
        print "Notify!"
        
    