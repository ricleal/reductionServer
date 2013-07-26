#!/usr/bin/python

import bottle
from bottle import route
import json
import pprint
import optparse
import tempfile
import sys
import sm.handler
import logging
import os.path

'''

Bottle reduction server

To test use curl:
-X GET | HEAD | POST | PUT | DELETE
Use curl -v for verbose


Assuming that one server will run for instrument and a single file is handled by the server.

'''

# Global variables
# load the logging configuration

LOGGING_CONF=os.path.join(os.path.dirname(__file__),"logging.ini")
from logging import config as _config
_config.fileConfig(LOGGING_CONF,disable_existing_loggers=False)
logger = logging.getLogger("server")

stateMachine = sm.handler.Handler()



@route('/', method='GET')
def homepage_get():
    '''
    Home page:
    
    Open with a browser or:
    curl http://localhost:8080/
    '''
    ret = '<html><h2>Yes I am up and running!</h2></html>'
    logger.debug('homepage_get')
    return ret

@route('/', method='POST')
def homepage_post():
    '''
    Home page
    
    curl -X POST  http://localhost:8080/
    
    '''
    logger.debug('homepage_post')
    return {'status' : 'Yes I am up and running!'}


@route('/status', method='POST')
def status():
    """
    Return server status
    
    Test:
    curl -X POST  http://localhost:8080/status 
    """
    status = stateMachine.status()
    
    logger.debug("Status: " + str(status))
    return status


# @route('/sendfile', method='POST')
# def sendfile():
#     '''
#     
#     Test: curl -X POST --data-binary @filename.nxs http://localhost:8080/sendfile
#     '''
#     
#     content = bottle.request.body.read()
#     
#     # Need to write the file on disk! there's no open stream in nexus library for python
#     tempFile = tempfile.NamedTemporaryFile(delete=False)
#     tempFile.write(content)
#     tempFile.close()
#   
#     try :
#         import nexus.handler as nx
#         nxHandler = nx.Handler(tempFile.name)  
#         print "Title read from the Nexus file:", nxHandler.title()
#         
#     except  Exception as e:
#         print "Error while reading the nexus file:", e
#         return {"status" : "KO", "message" : str(e) }
#     
#     try :
#         os.remove(tempFile.name)
#     except  Exception as e:
#         print "Error removing temporary nexus file:", e
#     
#     
#     return {"status" : "OK"}


@route('/file', method='POST')
def fileHandler():
    '''
    
    Test: curl -X POST --data-binary @filename.nxs http://localhost:8080/sendfile
    '''
    #stateMachine.sm().file(bottle.request)
    stateMachine.sm().receiveFile(bottle.request)
    
    status = stateMachine.status()
    
    print "Status", status
    return status

@route('/reset', method=['POST','GET'])
def reset():
    '''
    Clean up Nexus handler
    
    Test: curl -X POST http://localhost:8080/reset
    '''
    
    stateMachine.sm().reset()
    status = stateMachine.status()
    
    logger.debug("Status: " + str(status))
    return status

@route('/query', method='POST')
def query():
    '''
    
    curl -v -H "Content-Type: application/json" \
     -H "Accept: application/json"  \
     -X POST \
     -d '{"$toto":"cell", "$tata":"spacegroup", "$titi":"origin"}' \
     http://localhost:8080/query
    
    '''
    content = bottle.request.body.read()
    print 'Server received as json: ', content
    print 'See it as python dict:'
    contentAsDict = json.loads(content)
    
    stateMachine.sm().handleQuery(contentAsDict)
    
    status = stateMachine.status()
    
    print "Query result"
    return status


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
    
    # create state machine handler
    #     global stateMachine
    #     stateMachine = sm.handler.Handler()
    
    
    # Launch http server
    bottle.debug(True) 
    bottle.run(host=options.server, port=options.port)
    
if __name__ == '__main__':
    main(sys.argv)

    