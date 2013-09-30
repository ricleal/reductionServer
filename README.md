Reduction Server
===============

ILL REST Reduction Server

Prerequisites
-------------
  - Nexus python library : [http://www.nexusformat.org/](http://www.nexusformat.org/)
  - Python bottle : [http://bottlepy.org](http://bottlepy.org/)


Prerequisites for testing
-------------------------

  - Curl ([http://curl.haxx.se](http://curl.haxx.se/)). It is usually already installed by default in any modern Linux distribution.

At the ILL, in a Linux terminal, the following environent variables are often defined: `http_proxy` and `https_proxy`.

```bash
http_proxy="http://proxy.ill.fr:8888"
https_proxy="http://proxy.ill.fr:8888"
```

These variables must be `unset` for the curl POST requests to work within the ILL network!

Testing
-------------------------

**Start the server:**

```bash
# ./reductionServer.py -h
Usage: reductionServer.py [options]

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                        Server host. Default localhost.
  -p PORT, --port=PORT  Server port. Default 8080.
  -c CONFIG, --config=CONFIG
                        Configuration file. Default config.ini.
  -l LOG, --log=LOG     Logging configuration file. Default logging.ini.
```

Default ```.ini``` files are stored in the ```config``` directory.

E.g.:

```bash
./reductionServer.py -s localhost -p 8080
```

or the local hostname or the IP address. E.g.:

```bash
./reductionServer.py -s mypchostname.gen.ill.fr
```



**Test with a browser:**

Open the adress ```http://localhost:8080/``` in a browser.


**Test with curl client**

The server has been implemented with the following conditions:
- There will be a server per instrument. However, one machine can serve several instruments, as long as the servers are launched in different ports.
- Every NeXus file must be submitted to the server with the corresponding "Numor" as part of the URL. The numor can be seen as the unique identifier for every data set. See below the examples. 

Implemented functions to date:

This simple call can be performed by POST or GET. This is useful to see if the server is running from a http browser.

```bash
# Simple call with verbose active:
curl -v http://localhost:8080/

# Simple call by POST:
curl -X POST  http://localhost:8080/
```

The reduction procedure starts with the submission of a NeXus file and the respective numor.

A unique instance of a limited size dictionary ```DataStorage``` (inherited from [src/helper/dict.py](src/helper/dict.py) ) stores the pairs ```numor``` and ```NeXusHandler```. 
The same Nexus file can be submitted to the server as many times as desired. If the ```numor``` is already in the ```DataStorage``` the NeXus file handler will be updated, e.g., the old file will be deleted and replaced by the new one.

```bash
# Send a a binary nexus/hdf5 by post with the respective numor appended to the URL.
curl -X POST --data-binary @157589.nxs http://localhost:8080/file/157589
# Return
{"success": "OK"}
```

Once a NeXus file is submitted to the server, the reduction process can start.
This is done by sending *queries* in JSON format to the server. The format of the JSON queries is beeing defined. It may look like this:
```json
{
    "query": "sofqw",
    "input_parameters": [
        {
            "binning": [
                0.1,
                3,
                0.05
            ]
        },
        {
            "emode": "direct"
        }
    ],
    "numors": [
        10001,
        10002,
        10003
    ]
}
```

The nexus files affected by the query (and previously submitted) are identified by the field ```numors```.
A query identifier - universally unique identifier (UUID) - is returned for every query submited.

```bash
# Send a query to the server enclosing the JSON above. The curl header (-H) parameters are optional. Both curl and Bottle.py are clever enough to detect the content formats.
curl -v -H "Content-Type: application/json" \
         -H "Accept: application/json"  \
         -X POST \
         -d '{"query":"sofqw","input_parameters":[{"binning":[0.1,3,0.05]},{"emode":"direct"}],"numors":[10001,10002,10003]}' \
         http://localhost:8080/query
# Return:
{"query_id": "99faddc1-f089-4034-8599-9e4ce7d39c76"}
```

The ```query_id``` is used to fecth the results of a previously submitted query. The query submission details along with its results when fully processed are stored in the ```QueryStorage``` limited size dictionary. This dictionary is indexed by the UUID.
The results of a query can be fecthed through the request ```/results```:

```bash
# Now the client will ask for the results of the previous query:
curl -v -X POST http://localhost:8080/results/99faddc1-f089-4034-8599-9e4ce7d39c76
# Return
```
```json
{
    "status": "done",
    "executable": "ls -l",
    "start_time": 1379602228.618543,
    "return_code": 0,
    "start_local_time": "Thu Sep 19 16:50:28 2013",
    "end_local_time": "Thu Sep 19 16:50:28 2013",
    "query": "sofqw",
    "end_time": 1379602228.637719,
    "timeout": 10,
    "error": "",
    "numors": [
        8
    ],
    "output": "total 56\ndrwxr-xr-x 2 leal lss 4096 Sep 19 12:21 data\n-rw-r--r-- 1 leal lss  523 Sep 16 16:44 globalVars.pyc\ndrwxr-xr-x 2 leal lss 4096 Sep 19 11:12 helper\n-rw-r--r-- 1 leal lss  921 Jul 26 17:41 logging.ini\ndrwxr-xr-x 2 leal lss 4096 Sep 16 11:01 nexus\ndrwxr-xr-x 2 leal lss 4096 Sep 19 12:08 reduction\n-rwxr-xr-x 1 leal lss 5330 Sep 19 16:50 reductionServer.py\n-rw-r--r-- 1 leal lss 4864 Sep 12 11:55 reductionServer.pyc\n-rwxr-xr-x 1 leal lss 4113 Sep 19 16:42 test.py\n-rw-r--r-- 1 leal lss 4625 Aug  9 10:44 test.pyc\n"
}
```

Every *query* (e.g. *sofw*) will be mapped internally to an executable. In the example below the *sofqw* is mapped to ```"executable": "ls -l"```. This is still to be defined.

To get the status of all queries submitted to the server:
```bash
# This request can be either submitted by POST or GET
curl  http://localhost:8080/status
# Return
```
```json
{
  "7c772e56-afd2-4e05-ad6a-7beec625eeb0": "done", 
  "a388c27b-0227-4e6e-bb8f-328c9c93f99b": "done"
}
```

In the OS command line the JSON output can be formatted with the python command:
```bash
# Running curl in silent mode (-s : Don't show progress meter or error messages).
curl  -s http://localhost:8080/results/7c772e56-afd2-4e05-ad6a-7beec625eeb0 | python -mjson.tool

```

**Example:**

Let's submit 2 data files with 2 different numors:
```bash
curl -s -X POST --data-binary @102296.nxs http://localhost:8080/file/102296 | python -mjson.tool
```
```json
{
    "errors": "", 
    "general_message": "File successfully received.", 
    "success": "True"
}
```

```bash
curl -s -X POST --data-binary @102297.nxs http://localhost:8080/file/102297 | python -mjson.tool
```
```json
{
    "errors": "", 
    "general_message": "File successfully received.", 
    "success": "True"
}
```

Now let's submit a queries:

1. Inexistant function:

```bash
curl -s -X POST -d '{"function":"theta_vs_count","input_params":{"numors":[10229]}}'  http://localhost:8080/query | python -mjson.tool
```

```json
{
    "errors": {
        "exception_message": "u'theta_vs_count'", 
        "valid_functions": [
            "theta_vs_counts"
        ]
    }, 
    "general_message": "Error while validating the query function. Is it a valid function?", 
    "success": "False"
}

```

2. Invalid Numors:

```bash
curl -s -X POST -d '{"function":"theta_vs_counts","input_params":{"numors":[10229]}}'  http://localhost:8080/query | python -mjson.tool
```

```json
{
    "errors": {
        "invalid_numors": [
            10229
        ]
    }, 
    "general_message": "Numors do not exist in the database", 
    "success": "False"
}
```

3. Valid query

```bash
curl -s -X POST -d '{"function":"theta_vs_counts","input_params":{"numors":[102296]}}'  http://localhost:8080/query | python -mjson.tool
```

```json
{
    "query_id": "12c5faa1-661e-47a6-b56e-3eb4e2c026f4"
}
```

Query result:

```bash
curl -s http://localhost:8080/results/12c5faa1-661e-47a6-b56e-3eb4e2c026f4 | python -mjson.tool
```

```json
{
    "end_local_time": "Mon Sep 30 17:44:19 2013", 
    "end_time": 1380555859.450503, 
    "error": "", 
    "executable": "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh /tmp/tmpkaNAEI ", 
    "function": "theta_vs_counts", 
    "input_params": {
        "numors": [
            102296
        ]
    }, 
    "output": {
        "data_label": "Counts", 
        "data_shape": [
            1, 
            135
        ], 
        "data_units": "", 
        "data_values": [
            [
                0.0, 
                0.0, 
                0.0, 
                0.0, 
                0.0, 
                107.0, 
                (...)
                289.6976403687601, 
                158.0
            ]
        ], 
        "x_axis_label": "Scattering angle", 
        "x_axis_shape": [
            135
        ], 
        "x_axis_unit": "degrees", 
        "x_axis_values": [
            0.7091979356415034, 
            1.56893481993162, 
            2.540112536576862, 
            3.5110504074526236, 
            (...)
            132.4872807689507, 
            133.47312916428413, 
            134.3798613665934
        ]
    }, 
    "return_code": 0, 
    "start_local_time": "Mon Sep 30 17:44:08 2013", 
    "start_time": 1380555848.857111, 
    "status": "done", 
    "timeout": 30
}

```

**Test with unittest framework.**

The file ```test.py``` in the root of the project has unittest invoking all the implement requests. The client calls are coded in pycurl. Comments show how to call the same requests through the ```curl``` command line.

TODO
----

- A list of supported reduction functions available per instrument.
- A mapping between every function and the respective local executable.

To date, a simple JSON definition of a reduction function is available here: [src/data/functions.json](src/data/functions.json). More will come soon.

