ILL Live Data Reduction Server
===============

ILL REST Live data reduction server.

The purpose of this project is to bridge data acquisition and data analysis.
This server seats in the middle of the instrument control computer and the data reduction and analysis software.

The instrument control computer initiate the data analysis requests. The server reacts to these requests and forward the respective demands to the data analysis software. The server implements a Representational State Transfer (REST) with messages passed in [JSON](http://www.json.org/) format.


Prerequisites
-------------
  - Nexus python library : [http://www.nexusformat.org/](http://www.nexusformat.org/)
  - Python bottle : [http://bottlepy.org](http://bottlepy.org/)
  - PyMongo : [http://api.mongodb.org/python/](http://api.mongodb.org/python/). Use ```pip``` or ```easy_install```to install the last version. See [http://api.mongodb.org/python/current/installation.html](http://api.mongodb.org/python/current/installation.html)

Available methods
-----------------

The server implements the following methods:

- ```http:://<server_address>:<port>/file/<numor>```
    - Send a file or an URL to the server by POST identified by a <numor>. The server stores the file/url in the database indexed by the numor. 
- ```http:://<server_address>:<port>/query```
    - Send a query to the server indicating the data analysis routine to be called. See below the specs. The server returns and id for this query along with a foreseen timeout.
- ```http:://<server_address>:<port>/results/<queryId>``` - Interrogates the server about the result of query previously sent with queryId. This method can be called either by POST or GET.
- ```http:://<server_address>:<port>/status``` - Return the status of the queries in the server. 
- ```http:://<server_address>:<port>/methods``` - Return the methods details available for all instruments.
- ```http:://<server_address>:<port>/methodsavailable``` - Return the methods details available per this instrument.

A single server is launched by instrument. A single server only deals with a single data processing software, i.e., either Mantid or LAMP.
However, several servers can run in the same machine using different ports. The instrument name *MUST* be specified either in the configuration file, or when launching the server.  

Prerequisites for testing
-------------------------

- Curl ([http://curl.haxx.se](http://curl.haxx.se/)). It is usually already installed by default in any modern Linux distribution.

At the ILL, in a Linux terminal, the following environment variables are often defined: `http_proxy` and `https_proxy`.

```bash
http_proxy="http://proxy.ill.fr:8888"
https_proxy="http://proxy.ill.fr:8888"
```

For the curl POST requests to work within the ILL network, either these variables must be `unset` or the curl option ```--noproxy '*' ``` must be appended to the curl command.

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
  -c CONFIG, --config=CONFIG
                        Configuration file. Default config.ini.
  -l LOG, --log=LOG     Logging configuration file. Default logging.ini.
  -i INSTRUMENT, --instrument=INSTRUMENT
                        Intrument to server. If empty looks for instrument
                        name in the config file.
```
The config files (```.ini``` files) are stored in the ```config``` directory. Usually, for testing, those files do not need to be updated.

E.g.:

```bash
./reductionServer.py -s localhost -p 8080
```

or the local hostname or the IP address. E.g.:

```bash
./reductionServer.py -s mypchostname.gen.ill.fr
```

giving the instrument Name

```bash
./reductionServer.py -s 172.17.43.190 -p 8080 -i D20
```

**Test with a browser:**

Open the adress ```http://localhost:8080/``` in a browser.

The browser should show a json message similar to:
```json
{"message": "Server is up and running.", "details": "", "success": "True"}
```

**Test with curl client**

- GET:
```bash
$ curl --noproxy '*' -X GET  http://172.17.43.190:8080/
{"message": "Server is up and running.", "details": "", "success": "True"}
```
- POST:
```bash
$ curl --noproxy '*' -X POST  http://172.17.43.190:8080/
{"message": "Server is up and running.", "details": "", "success": "True"}
```
Additional option for ```curl```:

-   Verbose (```-v```) :

```bash
$ curl -v --noproxy '*' -X POST  http://172.17.43.190:8080/
* About to connect() to 172.17.43.190 port 8080 (#0)
*   Trying 172.17.43.190... connected
> POST / HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: 172.17.43.190:8080
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Date: Wed, 19 Mar 2014 11:09:41 GMT
< Server: WSGIServer/0.1 Python/2.7.3
< Content-Length: 74
< Content-Type: application/json
< 
* Closing connection #0
{"message": "Server is up and running.", "details": "", "success": "True"}
```

- Defining header (```-H```) :

```bash
$ curl -H "Accept: application/json"  --noproxy '*' -X POST  http://172.17.43.190:8080/
{"message": "Server is up and running.", "details": "", "success": "True"}
```

**Implemented functions to date**

Submitting URL :

```bash
$ curl --noproxy '*' -X POST --data "/home/leal/Documents/Mantid/IN5/094460.nxs" http://172.17.43.190:8080/file/094460
{"message": "File/URL successfully received.", "details": "The content is: Url", "success": "True"}
```
Submitting binary nexus file :

```bash
$ curl --noproxy '*' -X POST --data-binary @"/home/leal/Documents/Mantid/IN5/2014-03-19 -  dispersion peak/ILLIN5_Vana_095893.nxs" http://172.17.43.190:8080/file/095893
{"message": "File/URL successfully received.", "details": "The content is: NeXus", "success": "True"}
```

The reduction procedure starts with the submission of either physical data file (NeXus or Ascii) or a URL, and the respective numor.

The same file or URL can be submitted to the server as many times as desired. If the ```numor``` is already in the database the file handler will be updated, e.g., the old file (if a file is submitted) will be deleted and replaced by the new one.


Submitting a query for the previously submited numor 095893:

```bash
$ curl --noproxy '*' -X POST --data '{ "method" : "theta_vs_counts", "params" : { "numors":[095893]} }' http://172.17.43.190:8080/query
{"message": "Problems while validating the query...", "details": "JSON appears to be invalid.", "success": "False"}
```

Note that numors are passed as integers and are not json valid if are preceded by 0. The correct query should be:

```bash
$ curl --noproxy '*' -X POST --data '{ "method" : "theta_vs_counts", "params" : { "numors":[95893]} }' http://172.17.43.190:8080/query
{"query_id": "ac4605bd-1818-4a47-8407-bfef8f8031b9", "details": "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py", "timeout": 30}
```

A query identifier (query_id) - universally unique identifier (UUID) - along with a foreseen timeout is returned for every query submited.

Getting the query results for the query_id above:

```bash
$ curl --noproxy '*' -X GET http://172.17.43.190:8080/results/ac4605bd-1818-4a47-8407-bfef8f8031b9
{"status": "done", "input_params": {"data_file_full_path": "/tmp/live_A0RAaO.nxs", "instrument": "IN5", "data_file": "live_A0RAaO.nxs", "working_path": "/tmp"}, "executable": "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py", "start_time": "2014-03-19 12:24:03.267611", "start_local_time": "Wed Mar 19 12:24:03 2014", "end_local_time": "Wed Mar 19 12:24:21 2014", "instrument_name": "IN5", "end_time": "2014-03-19 12:24:21.776211", "timeout": 30, "queryId": "ac4605bd-1818-4a47-8407-bfef8f8031b9", "result": {"x_axis_values": [0.7091979356415034, (...),  54637.875642356776, 57166.32749483072, 48121.27000871812, 30504.04663524441, 9994.113718620729]], "x_axis_label": "Scattering angle", "x_axis_unit": "degrees", "x_axis_shape": [135], "data_units": ""}}
```

The json output can be formatted pipping the output to ```python -mjson.tool```:

```bash
$ curl --noproxy '*' -X GET http://172.17.43.190:8080/results/ac4605bd-1818-4a47-8407-bfef8f8031b9 | python -mjson.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5856  100  5856    0     0  2014k      0 --:--:-- --:--:-- --:--:-- 2859k
{
    "end_local_time": "Wed Mar 19 12:24:21 2014", 
    "end_time": "2014-03-19 12:24:21.776211", 
    "executable": "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py", 
    "input_params": {
        "data_file": "live_A0RAaO.nxs", 
        "data_file_full_path": "/tmp/live_A0RAaO.nxs", 
        "instrument": "IN5", 
        "working_path": "/tmp"
    }, 
    "instrument_name": "IN5", 
    "queryId": "ac4605bd-1818-4a47-8407-bfef8f8031b9", 
    "result": {
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
                (...),
                30504.04663524441, 
                9994.113718620729
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
            (...),
            133.47312916428413, 
            134.3798613665934
        ]
    }, 
    "start_local_time": "Wed Mar 19 12:24:03 2014", 
    "start_time": "2014-03-19 12:24:03.267611", 
    "status": "done", 
    "timeout": 30
}
```

One can also see the status of all queries stored in the server:

```bash
 curl --noproxy '*' -X GET http://172.17.43.190:8080/status | python -mjson.tool  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1905  100  1905    0     0   527k      0 --:--:-- --:--:-- --:--:--  620k
[
    {
        "end_local_time": "Fri Mar 14 15:13:30 2014", 
        "end_time": "2014-03-14 15:13:30.470509", 
        "executable": "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py", 
        "instrument_name": "IN5", 
        "queryId": "c22600bd-a84a-4752-904f-817f29ca5093", 
        "start_local_time": "Fri Mar 14 15:13:28 2014", 
        "start_time": "2014-03-14 15:13:28.382803", 
        "status": "done", 
        "timeout": 30
    }, 
    (.....), 
    {
        "end_local_time": "Wed Mar 19 12:24:21 2014", 
        "end_time": "2014-03-19 12:24:21.776211", 
        "executable": "/home/leal/git/reductionServer/src/query/scripts/theta_vs_counts_IN5.py", 
        "instrument_name": "IN5", 
        "queryId": "ac4605bd-1818-4a47-8407-bfef8f8031b9", 
        "start_local_time": "Wed Mar 19 12:24:03 2014", 
        "start_time": "2014-03-19 12:24:03.267611", 
        "status": "done", 
        "timeout": 30
    }
]

```

This simple call can be performed by POST or GET. This is useful to see if the server is running from a http browser.

```bash
# Simple call (by GET - default) with verbose active:
curl -v http://localhost:8080/

# Simple call by POST:
curl -X POST  http://localhost:8080/
```


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

Or a URL:
```bash
# Sent to the server URL.
curl --noproxy '*' -X POST --data /home/leal/Documents/Mantid/IN4/064727 http://localhost:8080/file/064727
# or
curl --noproxy '*' -X POST --data "file:///home/leal/Documents/Mantid/IN4/064727" http://localhost:8080/file/064727

# Return
```
```json
{
    "details": "", 
    "message": "File successfully received.", 
    "success": "True"
}
```

**Format of the queries**

The format of the JSON queries is still beeing defined. To date the valid format is:
```json
{
	"method" : "<method name to call>",
	"params" : {
		"name of the 1st input parameter" : <value : int, string, array, etc..>,
		"name of the 2nd input parameter" : <value : int, string, array, etc..>
	}
}
```
A working example is:

```json
{
	"method" : "theta_vs_counts",
	"params" : {
		"numors" : [
			94460,
			94461,
			94462
		]
	}
}
```
where the input parameter ```numors``` is one of the numors associated with a file or URL and previously submitted.

Adding new reduction scripts
----------------------------

In ```src/data``` two files exist with the local and remote definition of the queries to call.

-   The remote definition (```functions_remote.json```):

```json
{
	"theta_vs_counts" : {
		"description" : "Calculates the detector counts as a function of theta",
		"instruments" : [
			"IN4",
			"IN5",
			"IN6"
		],
		"params" : [
			{
				"name" : "numors",
				"type" : "array",
				"description" : "List of numors concerned"
			}
		],
		"output" : [
			{
				"name" : "plot",
				"type" : "plot_1d",
				"description" : "1D plot of theta vs counts",
				"units" : "NA"
			}
		]
	},
	"plot_data" : {
		"description" : "Plots raw data with corrections",
		"instruments" : [
			"D20"
		],
		"params" : [
			{
				"name" : "numors",
				"type" : "array",
				"description" : "List of numors concerned"
			}
		],
		"output" : [
			{
				"name" : "plot",
				"type" : "plot_1d",
				"description" : "1D plot of theta vs counts",
				"units" : "NA"
			}
		]
	}
}
```

-   The local definition (```functions_local.json```):

```json
{
	"theta_vs_counts" : {
		"timeout" : 30,
		"executable" : "%(scripts_directory)s/theta_vs_counts_%(instrument_name)s.py",
		"params" : [
			{
				"name" : "numors",
				"type" : "array",
				"description" : "List of numors concerned"
			}
		]
	},
	"plot_data" : {
		"timeout" : 40,
		"executable" : "%(scripts_directory)s/plot_data_%(instrument_name)s.prox",
		"params" : [
			{
				"name" : "numors",
				"type" : "array",
				"description" : "List of numors concerned"
			}
		]
	}
}
```

The variables ```scripts_directory``` and ```instrument_name``` will be assigned values in the ```config.ini``` file.


TODO
----

- A list of supported reduction functions available per instrument.
- A mapping between every function and the respective local executable.

- Put the Launcher PID in a list / database to kill if necessary.

Notes for me:
-------------
Check if the pc where the server is running has the port open:
```
[10:54 0.00 ~/tmp ]
[in6lnx2 27] tmp >  nmap -v -sT -PN 172.17.43.190
#or
nmap -v -p 8080 -PN 172.17.43.190
```

Launch server as:
```
./reductionServer.py -s 172.17.43.190 -p 8080
```

test it with:
```
curl -v --noproxy '*' http://172.17.43.190:8080/
```

