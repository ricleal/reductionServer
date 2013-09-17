#!/usr/bin/python

import bottle
from bottle import route
import json
import optparse
import sys
import logging
import os.path
import data.dataStorage
import data.queryStorage
import nexus.nexusHandler
import time
import signal
import uuid
import simplejson

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


# Handle signals

# def signal_handler(signal_, frame):
#     logger.info("Server caught a signal! Server is shutting down...")
#     global queryManager
#     #time.sleep(1)
#     queryManager.exit()
#     #time.sleep(1)
#     queryManager.join()
#     #os.kill(os.getpid(), signal.SIGTERM)
#     logger.info("Server shut down!")
#     sys.exit(0)
#     
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

@route('/', method=['GET','POST'])
def homepage_get():
    '''
    Home page:
    
    Open with a browser or:
    curl http://localhost:8080/
    '''
    logger.debug('Home page was requested.')
    return


@route('/file/<numor:int>', method='POST')
def fileHandler(numor):
    '''
    To test:
    
    cd ~/Documents/Mantid/IN6
    curl -X POST --data-binary @157589.nxs http://localhost:8080/file/<numor>
    '''
    
    successMsg = {"success" : "OK"}
    
    logger.debug("Receiving Nexus file by POST with numor = %d" % numor)
    
    content = bottle.request.body.read()
    nexusHandler = nexus.nexusHandler.NeXusHandler(content)
    
    from data.dataStorage import dataStorage
    dataStorage[numor] = nexusHandler
    
    logger.debug(str(dataStorage))
    return successMsg

#@route('/query/<numors:re:[0-9,]+>', method='POST')
@route('/query', method='POST')
def query():
    '''
    
    curl -v -H "Content-Type: application/json" \
     -H "Accept: application/json"  \
     -X POST \
     -d '{"query":"plot", "axes":"x,y"}' \
     http://localhost:8080/query>
     
    '''
    
    content = bottle.request.body.read()
        
    contentAsDict = json.loads(content)
    logger.debug("Query received: " + str(contentAsDict))
    
    # TODO: validate query:
    
    uniqId = str(uuid.uuid4())
    from data.queryStorage import queryStorage
    queryStorage.addQuery(uniqId,content)
    
    #TODO: handle query
    
    
    
    
    return {"query_id" : uniqId}

@route('/results/<queryId>', method=['POST','GET'])
def results(queryId):
    """
    Return the contents of localDataStorage has json
    
    Test:
    curl -X POST  http://localhost:8080/results/<queryId>
    """
    
    from data.queryStorage import queryStorage
    thisQuery = queryStorage[queryId]
    
    
    print thisQuery
    
    return simplejson.dumps(thisQuery)





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
    
    #
    dataStorage = data.dataStorage.DataStorage(size_limit=22)
    queryStorage = data.queryStorage.QueryStorage(size_limit=256)
    
    # Launch http server
    bottle.debug(True) 
    bottle.run(host=options.server, port=options.port)
    print "Server stopped..."
    
    
if __name__ == '__main__':
    main(sys.argv)

    