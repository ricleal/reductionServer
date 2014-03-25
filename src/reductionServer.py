#!/usr/bin/python

import bottle
from bottle import route

import sys
import logging
import time
import signal


import config.config

import data.messages
from content.validator.filename import FileValidator
from query.handler import QueryHandler
from result.handler import HandlerResult
from status.handler import HandlerStatus
from methods.handler import HandlerMethods

'''

Bottle reduction server

To old_test use curl:
-X GET | HEAD | POST | PUT | DELETE
Use curl -v for verbose

It assumes:
    - One server will run for a single instrument
    - Just a single file is handled by the server at the same time.
        - The submission of new file will invalidates the stored data of the previous one

'''



logger = logging.getLogger("server")


# Handle signals
def signal_handler(signal_, frame):
    logger.info("Server caught a signal! Server is shutting down...")
    logger.info("Killing running processes...")
    
    # TODO
    # Any cleanups needed
    
    time.sleep(0.1)
    
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
    return data.messages.Messages.success("Server is up and running.")


@route('/file/<numor:int>', method='POST')
def fileHandler(numor):
    '''
    
    User can send a binary / ascii file or an url for a file location.
    
    To test:
    
    curl -v --noproxy '*' -X POST --data-binary @094460.nxs http://localhost:8080/file/094460

    curl -v --noproxy '*' -X POST --data "`pwd`" http://localhost:8080/file/094460
    
    '''
    
    logger.debug("Receiving file by HTTP POST with numor = %d" % numor)
    
    content = bottle.request.body.read()
    
    v = FileValidator(content)
    message = v.validateFile(numor)
    
    logger.debug(message)
    return message
    
    
#@route('/query/<numors:re:[0-9,]+>', method='POST')
@route('/query', method='POST')
def query():
    '''
    Get the query results. Sent json by the client should be of the form:
    { "method" : "theta_vs_counts", "params" : { "numors":[94460]} }
    '''
    
    content = bottle.request.body.read()
    logger.debug("RAW Query received: " + str(content))
    
    qh = QueryHandler(content)
    message = qh.process()
    logger.debug(message)
    return message
    
    

@route('/results/<queryId>', method=['POST','GET'])
def results(queryId):
    """
    Return the contents of localDataStorage has json
    
    Test:
    curl -X POST  http://localhost:8080/results/<queryId>
    """
            
    r = HandlerResult(queryId)
    message = r.getQuery()
    logger.debug(message)
    return message
    
@route('/resultszipped/<queryId>', method=['POST','GET'])
def resultszipped(queryId):
    """
    Return the contents of localDataStorage has json
    
    Test:
    curl -X POST  http://localhost:8080/resultszipped/<queryId>
    """
            
    r = HandlerResult(queryId)
    message = r.getQueryZipped()
    logger.debug("Zipped content! size = %d"%len(message))
    bottle.response.set_header('Content-Encoding', 'gzip')
    return message


@route('/status', method=['POST','GET'])
def status():
    """
    Returns data of queries
    """
    
    r = HandlerStatus()
    message = r.getQueries()
    logger.debug(message)
    return message

@route('/methods', method=['POST','GET'])
def methods():
    h = HandlerMethods()
    message = h.getAllMethods()
    logger.debug(message)
    return message
    
@route('/methodsavailable', method=['POST','GET'])
def methodsAvailable():
    h = HandlerMethods()
    message = h.getMethodsForThisInstrument()
    logger.debug(message)
    return message



def main(argv):
    # command line options
    from config.config import options
        
    # Launch http server
    bottle.debug(True)
    
    try :
        bottle.run(host=options.server, port=options.port)
    except Exception as e:
        #logger.exception("Web server cannot run: " + str(e)) 
        logger.error("Web server cannot run: " + str(e))
    
    logger.info("Server shutdown...")
    
if __name__ == '__main__':
    main(sys.argv)

    