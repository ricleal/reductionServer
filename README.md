Reduction Server
===============

ILL REST Reduction server

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
- There will be a server per instrument. However, one machine can server several instruments, as long as the server are launched with different ports.
- Every NeXus file must be submitted to the server with the corresponding "Numor" in the HTTP header. The numor can be seen as the unique id of every data set. See below th example. 

Implemented functions to date:

```
# Simple call with verbose active:
curl -v http://localhost:8080/

# Simple call by POST:
curl -X POST  http://localhost:8080/

# Send a a binary nexus/hdf5 by post. Note the "Numor" header.
curl -X POST -H "Numor: 1234"  --data-binary @157589.nxs http://localhost:8080/file
# Return:
{"numor": "1234"}

# Send a query to the server. Here the client is asking to put in the variables $toto and $tata the result of calling func1() and func2('par'). 
curl -v -H "Content-Type: application/json" \
        -H "Numor: 1234" \
         -H "Accept: application/json"  \
         -X POST \
         -d '{"$toto":"func1()", "$tata":"func2(\"par\")"}' \
         http://localhost:8080/query
# Return:
{u'$toto': {'status': 'querying', 'query': u'func1()', 'value': None, 'desc': None}, 'numor': '1234', u'$tata': {'status': 'querying', 'query': u"func2('par')", 'value': None, 'desc': None}}         

# Now the client will ask for the results of the previous query:
curl -v -X POST http://localhost:8080/results
# Return
{u'$toto': {'status': 'Done', 'query': u'func1()', 'value': 'ret func1', 'desc': None}, 'numor': '1234', u'$tata': {'status': 'Done', 'query': u"func2('par')", 'value': 'ret func2', 'desc': None}
```

**Test with unittest framework.**

The file test.py in the root of the project has a a test invoking all the requested above coded in pycurl.

