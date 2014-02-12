#!/usr/bin/python

import bottle
from bottle import route
import json
import sys
import logging
import os.path
import contenthandlers.handlermanager
import time
import signal
import uuid
import simplejson
import pprint

import data.dataStorage
import data.queryStorage
import data.queryValidator
import reduction.queryLauncher
import data.messages

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

import config.config

logger = logging.getLogger("server")


# Handle signals
def signal_handler(signal_, frame):
    logger.info("Server caught a signal! Server is shutting down...")
    logger.info("Killing running processes...")
    
    queryManager = reduction.queryLauncher.QueryLauncher()
    queryManager.killAllRunningLaunchers()
    
    # delete temporary nexus files
    from data.dataStorage import dataStorage
    dataStorage.deleteContent()
    
    time.sleep(1)
    
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
    To test:
    
    cd ~/Documents/Mantid/IN6
    curl -X POST --data-binary @157589.nxs http://localhost:8080/file/<numor>
    '''
    
    logger.debug("Receiving file by HTTP POST with numor = %d" % numor)
    
    content = bottle.request.body.read()
    # based on the content get the right file handler
    handlerManager = contenthandlers.handlermanager.Manager(content)
    fileHandler = handlerManager.getRespectiveHandler()
    
    if fileHandler is None:
        return data.messages.Messages.error("File received is not valid", "Neither ASCII nor Nexus");
    else:
        from data.storage import Storage
        db = Storage()
        db.insertOrUpdateNumor(numor, fileHandler.filename())
        return data.messages.Messages.success("File successfully received.", "The handler is: " + fileHandler.__class__.__name__)

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
    
    logger.debug("RAW Query received: " + str(content))
        
    try :
        contentAsDict = json.loads(content)
    except Exception, e:
        message = "JSON appears to be invalid."
        logger.exception(message  + str(e))
        return data.messages.Messages.error(message,str(e))
    
    logger.debug("FORMATTED Query received: " + str(contentAsDict))
    
    
    queryValidator = data.queryValidator.QueryValidator(contentAsDict)
    
    validErrorMessage = queryValidator.validateFunction()
    if validErrorMessage is not None :
        return validErrorMessage
    
    validErrorMessage = queryValidator.validateNumors()
    if validErrorMessage is not None :
        return validErrorMessage
    
    queryId = str(uuid.uuid4())
    from data.queryStorage import queryStorage
    queryStorage.addQuery(queryId,contentAsDict)
    
    logger.debug("QueryStorage:\n" + pprint.pformat(queryStorage.items()))
    
    #TODO: handle query
    queryStorage[queryId]["executable"] = queryValidator.getExecutable() 
    queryStorage[queryId]["timeout"] = queryValidator.getExecutableTimeout()
    
    q = reduction.queryLauncher.QueryLauncher()
    q.processQuery(queryId)
    
    logger.debug("DataStorage:\n" + pprint.pformat(queryStorage.items()))
    
    return {"query_id" : queryId}

@route('/results/<queryId>', method=['POST','GET'])
def results(queryId):
    """
    Return the contents of localDataStorage has json
    
    Test:
    curl -X POST  http://localhost:8080/results/<queryId>
    """
    
    from data.queryStorage import queryStorage
    try:
        thisQuery = queryStorage[queryId].copy() # copy by value
        logger.debug("This Query:\n" + pprint.pformat(thisQuery))
        del thisQuery["launcher"] # Json can't serialise objects!
        return simplejson.dumps(thisQuery)
    except Exception, e:
        message = "query_id appears to be invalid."
        logger.exception(message  + str(e))
        return data.messages.Messages.error(message,str(e))
    

@route('/status', method=['POST','GET'])
def status():
    """
    Returns pairs of query_ids = status
    """
    ret = {"dataStorage":{},"queryStorage":{}}
    
    from data.dataStorage import dataStorage
    
    for k in dataStorage.keys():
        try:
            ret["dataStorage"][k] = '%s'%dataStorage[k]
        except:
            pass
    
    
    from data.queryStorage import queryStorage
    
    
    for k in queryStorage.keys():
        try:
            ret["queryStorage"][k] = queryStorage[k]["status"]
        except:
            pass
    
    logger.debug("Satus:\n" + pprint.pformat(ret))
    return ret


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

    