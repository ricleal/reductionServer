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

Default ```.ini``` files are stored in the ```config``` directory. Usually the logging.ini does not need to be updated.

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

**Implemented functions to date**

This simple call can be performed by POST or GET. This is useful to see if the server is running from a http browser.

```bash
# Simple call (by GET - default) with verbose active:
curl -v http://localhost:8080/

# Simple call by POST:
curl -X POST  http://localhost:8080/
```

The reduction procedure starts with the submission of a NeXus file and the respective numor.

A unique instance of a limited size dictionary ```DataStorage```:
```python
from data.dataStorage import dataStorage
```
(inherited from [src/helper/dict.py](src/helper/dict.py) ) stores the pairs ```numor``` and ```NeXusHandler```. 
The same Nexus file can be submitted to the server as many times as desired. If the ```numor``` is already in the ```DataStorage``` the NeXus file handler will be updated, e.g., the old file will be deleted and replaced by the new one.

```bash
# Send a a binary nexus/hdf5 file by post with the respective numor appended to the URL.
curl -X POST --data-binary @157589.nxs http://localhost:8080/file/157589
# Return
```
```json
{
    "details": "", 
    "message": "File successfully received.", 
    "success": "True"
}

```

Once a NeXus file is submitted to the server, the reduction process can start.
This is performed by submiting JSON *queries* to the server. The format of the JSON queries is still beeing defined. To date the valid format is:
```json
{
	"function":"<function name>",
	"input_params":{
		[
		"<parameter name>":<parameter value>,
		"<parameter name>":<parameter value>,
		(...)
		]
		
	}
}
```
A working example is:

```json
{
	"function":"theta_vs_counts",
	"input_params":{
		"numors":[
			12345,
            56789,
            12121
		]
		
	}
}
```
where the input parameter ```numors``` is one of the numors associated with a nexus file and previously submitted.

A query identifier - universally unique identifier (UUID) - is returned for every query submited.

```bash
# Send a query to the server enclosing the JSON above. The curl header (-H) parameters are optional. Both curl and Bottle.py are clever enough to detect the content formats.
curl -v -H "Content-Type: application/json" \
        -H "Accept: application/json"  \
        -X POST \
        -d  '{"function":"theta_vs_counts","input_params":{"numors":[102296]}}' \
        http://localhost:8080/query
# Return:
```
```json
{
    "query_id": "4b800405-3332-466a-be83-e6e6e0905ae4"
}
```

If an invalid query (invalid function name) is submitted to the server the result is:

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

If invalid input parameters (numors in this case) are sent in the query, the result is:

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

The ```query_id``` is used to fecth the results of a previously submitted query. The query submission details along with its results when fully processed are stored in the ```QueryStorage``` limited size dictionary:

```python
from data.queryStorage import queryStorage
```

This dictionary is indexed by the UUID.

The results of a query can be fecthed through the request ```/results```:

```bash
# Now the client will ask for the results of the previous query:
curl -v -X POST http://localhost:8080/results/4b800405-3332-466a-be83-e6e6e0905ae4
```

The result of this request is the status of the query. When the processing of the query is still running the returned json looks similar to:

```json
{
    "executable": "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh /tmp/live_D2lycx.nxs ", 
    "function": "theta_vs_counts", 
    "input_params": {
        "numors": [
            102296
        ]
    }, 
    "start_time": "2013-10-02 12:13:25.125645",
    "status": "running", 
    "timeout": 30
}

```

When it is done:

```json
{
    "end_time": "2013-10-02 12:13:35.464550", 
    "error": "", 
    "executable": "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh /tmp/live_D2lycx.nxs ", 
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
(..) 
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
(..)
            133.47312916428413, 
            134.3798613665934
        ]
    }, 
    "return_code": 0, 
    "start_time": "2013-10-02 12:13:25.125645", 
    "status": "done", 
    "timeout": 30
}

```

In the previous case the output is a plot.

When a query is invalid:
```json
{
    "details": "'dde5971c-a189-4532-a06a-7bc02b5a56f'", 
    "message": "query_id appears to be invalid.", 
    "success": "False"
}

```

Every *query* (e.g. *theta_vs_counts*) will be mapped internally to an executable. In the example below the *sofqw* is mapped to ```"executable": "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh"```. 

To get the status of all queries submitted to the server along with the files:
```bash
# This request can be either submitted by POST or GET
curl  http://localhost:8080/status
# Return
```
```json
{
    "dataStorage": {
        "102296": "/tmp/live_LhAVdL.nxs", 
        "102297": "/tmp/live_A6Qpvm.nxs"
    }, 
    "queryStorage": {
        "a5573866-f687-49bd-87bd-56e4f5851baf": "done"
    }
}
```

In the OS command line the JSON output can be formatted pipping the python command ```python -mjson.tool```:
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
    "details": "", 
    "message": "File successfully received.", 
    "success": "True"
}

```

```bash
curl -s -X POST --data-binary @102297.nxs http://localhost:8080/file/102297 | python -mjson.tool
```
```json
{
    "details": "", 
    "message": "File successfully received.", 
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
    "end_time": "2013-10-02 12:13:35.464550", 
    "error": "", 
    "executable": "/home/leal/git/reductionServer/scripts/theta_vs_counts_IN5.sh /tmp/live_D2lycx.nxs ", 
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
                26630.440714397362, 
                73900.37826959942, 
                (...)
                1202.3282591853645, 
                585.4388730584927, 
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
            4.507464014742497, 
            (..)
            132.4872807689507, 
            133.47312916428413, 
            134.3798613665934
        ]
    }, 
    "return_code": 0, 
    "start_time": "2013-10-02 12:13:25.125645", 
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
