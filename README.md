Reduction Server
===============

ILL REST Reduction server

Prerequisites
-------------
  - Nexus python library : [http://www.nexusformat.org/](http://www.nexusformat.org/)
  - Python bottle : [http://bottlepy.org](http://bottlepy.org/)

At the ILL don't forget to set the environent variable `http_proxy` and `https_proxy`. E.g.:

```
export http_proxy="http://proxy.ill.fr:8888"
export https_proxy="http://proxy.ill.fr:8888"
```

Prerequisites for testing
-------------------------

  - Curl ([http://curl.haxx.se](http://curl.haxx.se/)). It is normally already installed by default in any modern Linux distribution.


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
# ./reductionServer.py -s localhost -p 8080
```

**Test with a browser:**

Open the adress ```http://localhost:8080/``` in a browser.


**Test with curl client**

Implemented functions to date:

```
# Simple call:
curl http://localhost:8080/

# Simple call by POST with json response:
curl -X POST  http://localhost:8080/

# Server status
curl -X POST  http://localhost:8080/status

# Send a binary nexus/hdf5 file to the server:
curl -X POST --data-binary @filename.nxs http://localhost:8080/sendfile

# Send json content with verbode and predefined content types:
curl -v -H "Content-Type: application/json" \
	-H "Accept: application/json"  \
    -X POST \
    -d '{"$toto":"cell", "$tata":"spacegroup", "$titi":"origin"}' \
    http://localhost:8080/getvariables

```


