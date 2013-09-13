#!/usr/bin/python

import bottle
from bottle import route
import json
import optparse
import sys
import logging
import os.path
import data.dataStorage
import nexus.nexusHandler
import reduction.threadManager
import time
import signal
import uuid

'''

Bottle reduction server

To test use curl:
-X GET | HEAD | POST | PUT | DELETE
Use curl -v for verbose

It assumes:
    - One server will run for a single instrument
    - Just a single file is handled by the server at the same time.
        - The submission of new file will invalidates the stored data of the previous one

'''

# Global variables
# load the logging configuration

LOGGING_CONF=os.path.join(os.path.dirname(__file__),"logging.ini")
 
from logging import config as _config
_config.fileConfig(LOGGING_CONF,disable_existing_loggers=False)

logger = logging.getLogger("server")

threadManager = None

# Handle signals

def signal_handler(signal_, frame):
    logger.info("Server caught a signal! Server is shutting down...")
    global threadManager
    #time.sleep(1)
    threadManager.exit()
    #time.sleep(1)
    threadManager.join()
    #os.kill(os.getpid(), signal.SIGTERM)
    logger.info("Server shut down!")
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@route('/', method=['GET','POST'])
def homepage_get():
    '''
    Home page:
    
    Open with a browser or:
    curl http://localhost:8080/
    '''
    logger.debug('Home page was requested.')
    return


@route('/file', method='POST')
def fileHandler():
    '''
    To test:
    
    cd ~/Documents/Mantid/IN6
    curl -X POST -H "Numor: 1234"  --data-binary @157589.nxs http://localhost:8080/file
    '''
    
    
    content = bottle.request.body.read()
    
    numor =  bottle.request.get_header('Numor', None)
    
    logger.debug("Receiving file POST. Numor = " + str(numor))
    
    localDataStorage = data.dataStorage.DataStorage()
    if numor is not None and (localDataStorage.empty() or localDataStorage.getNumor() != numor):
        # create a new data storage!
        localDataStorage.setNumor(numor)
        # TODO:
        # Code the removeAllThreads function!
        global threadManager
        threadManager.removeAllThreads()
        
    # always update the nexus data (the next file may have more counts!)
    nexusHandler = nexus.nexusHandler.NeXusHandler(content)
    localDataStorage.setNexusHandler(nexusHandler)
    
    return localDataStorage.toJson()


@route('/results', method=['POST','GET'])
def results():
    """
    Return the contents of localDataStorage has json
    
    Test:
    curl -X POST  http://localhost:8080/results 
    """
    
    localDataStorage = data.dataStorage.DataStorage()
        
    logger.debug("Sending results to client...")
    logger.debug("Local Storage: \n" + str(localDataStorage))
    
    return localDataStorage.toJson()


@route('/query', method='POST')
def query():
    '''
    
    curl -v -H "Content-Type: application/json" \
    -H "Numor: 1234" \
     -H "Accept: application/json"  \
     -X POST \
     -d '{"$toto":"cell", "$tata":"spacegroup", "$titi":"origin"}' \
     http://localhost:8080/query
    
    '''
    global threadManager

    content = bottle.request.body.read()
    numor =  bottle.request.get_header('Numor', None)
    
    contentAsDict = json.loads(content)
    logger.debug("Query received: " + str(contentAsDict))
    localDataStorage = data.dataStorage.DataStorage()
    logger.debug("Local Storage: " + str(localDataStorage))
    
    uniqId = uuid.uuid4()
    
    # update local storage with the queries
    if numor is not None and not localDataStorage.empty() and localDataStorage.getNumor() == numor:
        for variable,query in contentAsDict.items():
            # Launching the process
            threadManager.addThread(variable, query)

            
    
    logger.debug("Local Storage: \n" + str(localDataStorage))
    return localDataStorage.toJson()


def commandLineOptions():
    '''
    Define command line options
    '''
    parser = optparse.OptionParser()
    parser.add_option('-s', '--server', help='Server host. Default localhost.', default='localhost')
    parser.add_option('-p', '--port', help='Server port. Default 8080.', type="int", default=8080)
    return parser

def main(argv):
    parser = commandLineOptions();
    (options, args) = parser.parse_args()
    
    # thread manager
    global threadManager
    threadManager = reduction.threadManager.ThreadManager()
    threadManager.start()
     
    # Launch http server
    bottle.debug(True) 
    bottle.run(host=options.server, port=options.port)
    print "Server stopped..."
    
    
if __name__ == '__main__':
    main(sys.argv)

    