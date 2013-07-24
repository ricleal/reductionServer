#!/usr/bin/python

import bottle
from bottle import route
import json
import pprint
import optparse
import tempfile
import os

'''

Bottle reduction server

To test use curl:
-X GET | HEAD | POST | PUT | DELETE

Use curl -v for verbose

TODO:

Define status

'''

@route('/', method='GET')
def homepage_get():
    '''
    Home page:
    
    Open with a browser or:
    curl http://localhost:8080/
    '''
    return '<html><h2>Yes I am up and running!</h2></html>'

@route('/', method='POST')
def homepage_get():
    '''
    Home page
    
    curl -X POST  http://localhost:8080/
    
    '''
    return {'status' : 'Yes I am up and running!'}


@route('/status', method='POST')
def status():
    """
    Return server status
    
    Test:
    curl -X POST  http://localhost:8080/status 
    """
    rv = {"status" : "waiting"}
    return rv


@route('/sendfile', method='POST')
def sendfile():
    '''
    
    Test: curl -X POST --data-binary @filename.nxs http://localhost:8080/sendfile
    '''
    
    content = bottle.request.body.read()
    
    # Need to write the file on disk! there's no open stream in nexus library for python
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    tempFile.write(content)
    tempFile.close()
  
    try :
        import nexus.handler as nx
        nxHandler = nx.Handler(tempFile.name)  
        print "Title read from the Nexus file:", nxHandler.title()
        
    except  Exception as e:
        print "Error while reading the nexus file:", e
        return {"status" : "KO", "message" : str(e) }
    
    try :
        os.remove(tempFile.name)
    except  Exception as e:
        print "Error removing temporary nexus file:", e
    
    
    return {"status" : "OK"}


@route('/getvariables', method='POST')
def getvariables():
    '''
    
    curl -v -H "Content-Type: application/json" \
     -H "Accept: application/json"  \
     -X POST \
     -d '{"$toto":"cell", "$tata":"spacegroup", "$titi":"origin"}' \
     http://localhost:8080/getvariables
    
    '''
    
    content = bottle.request.body.read()
    print 'Server received as json: ', content
    print 'See it as python dict:'
    contentAsDict = json.loads(content)
    pprint.pprint(contentAsDict,indent=4,depth=2)
    
    ## Do required calculations
    
    return { "$toto" : [10,10,10,90,90,90], "$tata" : 178, "$titi" : [0, 0, 0] }

def commandLineOptions():
    '''
    Define command line options
    '''
    parser = optparse.OptionParser()
    parser.add_option('-s', '--server', help='Server host. Default localhost.', default='localhost')
    parser.add_option('-p', '--port', help='Server port. Default 8080.', type="int", default=8080)
    return parser

if __name__ == '__main__':
    parser = commandLineOptions();
    (options, args) = parser.parse_args()
    
    # Launch http server
    bottle.debug(True) 
    bottle.run(host=options.server, port=options.port)

    