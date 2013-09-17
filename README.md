Reduction Server
===============

ILL REST Reduction Server

Prerequisites
-------------
  - Nexus python library : [http://www.nexusformat.org/](http://www.nexusformat.org/)
  - Python bottle : [http://bottlepy.org](http://bottlepy.org/)


Prerequisites for testing
-------------------------

  - Curl ([http://curl.haxx.se](http://curl.haxx.se/)). It is normally already installed by default in any modern Linux distribution.

At the ILL, in a Linux terminal, usually the following environent variables are defined: `http_proxy` and `https_proxy`.

```
http_proxy="http://proxy.ill.fr:8888"
https_proxy="http://proxy.ill.fr:8888"
```

These variables must be `unset` for the curl POST requests to work within the ILL network!

Testing
-------------------------

**Start the server:**

```
# ./reductionServer.py -h
Usage: reductionServer.py [options]

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                        Server host. Default localhost.
  -p PORT, --port=PORT  Server port. Default 8080.
```

E.g.:

```
./reductionServer.py -s localhost -p 8080
```

or the local hostname or the IP address. E.g.:

```
./reductionServer.py -s mypchostname.gen.ill.fr
```



**Test with a browser:**

Open the adress ```http://localhost:8080/``` in a browser.


**Test with curl client**

The server has been implemented with the following conditions:
- There will be a server per instrument. However, one machine can serve several instruments, as long as the servers are launched in different ports.
- Every NeXus file must be submitted to the server with the corresponding "Numor" in the HTTP header. The numor can be seen as the unique id of every data set. See below the examples. 

Implemented functions to date:

This simple call can be performed by POST or GET. This is useful to see if the server is running from a http browser.

```
# Simple call with verbose active:
curl -v http://localhost:8080/

# Simple call by POST:
curl -X POST  http://localhost:8080/
```

The reduction procedure starts with with the submission of a NeXus file with the http header "Numor: <ILL generated numor>".
A unique [Borg Singleton](http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/) is created ```data.dataStorage``` to store the status of the reduction procedure.
The same Nexus file can be submitted to the server as many times as desired.

```
# Send a a binary nexus/hdf5 by post with the respective numor appended to the URL.
curl -X POST --data-binary @157589.nxs http://localhost:8080/file/157589
# Return:
{"numor": "1234"}
```

Once a NeXus file is submitted to the server, the reduction process can start.
This is done by sending pairs of ```<variable name> : <function to be called in the reduction server>```. 
This functions will be called in threads managed by the ```reduction.threadManager```. The threadManager will monitor the functions and eventually remove the timed out requests.

```
# Send a query to the server. The URL must be appended with the numor(s) used by the query. If multiple numors are used, then they must be separated by a comma ```,```.
Here the client is asking to put in the variables $toto and $tata the result of calling func1() and func2('par'). 
curl -v -H "Content-Type: application/json" \
         -H "Accept: application/json"  \
         -X POST \
         -d '{"$toto":"func1()", "$tata":"func2(\"par\")"}' \
         http://localhost:8080/query/12345,12346,12347
# Return:
{u'$toto': {'status': 'querying', 'query': u'func1()', 'value': None, 'desc': None}, 'numor': '1234', u'$tata': {'status': 'querying', 'query': u"func2('par')", 'value': None, 'desc': None}}         
```

The monitoring of the server can be done through the request ```/results```. This will return several JSON fields including the result of the called function ```value``` as well as the ```status``` of the query.

```
# Now the client will ask for the results of the previous query:
curl -v -X POST http://localhost:8080/results
# Return
{u'$toto': {'status': 'Done', 'query': u'func1()', 'value': 'ret func1', 'desc': None}, 'numor': '1234', u'$tata': {'status': 'Done', 'query': u"func2('par')", 'value': 'ret func2', 'desc': None}
```

**Test with unittest framework.**

The file ```test.py``` in the root of the project has unittest invoking all the implement requests. The client calls are coded in pycurl. Comments show how to call the same requests through the ```curl``` command line.

TODO
----

A list of supported reduction functions available per instrument.

To date, a simple JSON definition of a reduction function is available here: [src/data/functions.json](src/data/functions.json). More will come soon.

