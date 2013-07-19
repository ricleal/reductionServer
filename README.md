Reduction Server
===============

ILL REST Reduction server

Prerequisites
-------------
  - Nexus python library [http://www.nexusformat.org/](http://www.nexusformat.org/)
  - Python bottle [http://bottlepy.org](http://bottlepy.org/)

At the ILL don't forget to set the environent variable `http_proxy` and `https_proxy`. E.g.:

```
export http_proxy="http://proxy.ill.fr:8888"
export https_proxy="http://proxy.ill.fr:8888"
```

Prerequisites for testing
-------------------------

  - Curl [http://curl.haxx.se](http://curl.haxx.se/). It should be installed by default in any modern Linux distribution.

```
# To send a binary file to the server:
curl -X POST --data-binary @filename.nxs http://localhost:8080/sendfile
# To send json content with verbode and predefined content types:
curl -v -H "Content-Type: application/json" \
	-H "Accept: application/json"  \
    -X POST \
    -d '{"$toto":"cell", "$tata":"spacegroup", "$titi":"origin"}' \
    http://localhost:8080/getvariables
```
