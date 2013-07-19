import bottle
from bottle import route
import json
import pprint
'''

Bottle reduction server

To test use curl:
-X GET | HEAD | POST | PUT | DELETE

Use curl -v for verbose

TODO:

Define status

'''

@route('/', method='GET')
def homepage():
    '''
    Home page
    '''
    return '<h2>Yes I am up and running! </h2>'

@route('/status', method='GET')
def status():
    """
    Return server status
    
    Test:
    curl -X GET  http://localhost:8080/status > /tmp/out.txt ; cat /tmp/out.txt 
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
    filename = "/tmp/tmp.nxs"
    with open(filename, 'wb') as f:
        f.write(content)
            
    try :
        import nxs
        nexusFile = nxs.open(filename,'r')
        nexusFile.opengroup('entry0')
        nexusFile.opendata('title')
        print "Title read from the Nexus file:", nexusFile.getdata()
        nexusFile.close()
        
    except  Exception as inst:
        print "Unexpected error:", inst
        return {"status" : "KO", "message" : str(inst) }
    
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


bottle.debug(True) 
bottle.run(host='localhost', port=8080)