# AsyncCall package

This package contains the interface between the server and the reduction packages call.

LaunchManager is the only class needed to send commands and get the results from the reduction software.
See testManager.py to see how it worsks.

## Diagram for Launcher class hierarchy


	+------------------------+
	|        Launcher        |
	|------------------------|
	| __metaclass__          |
	| __initParams           |
	|------------------------|
	| __init__               |
	| sendCommand            |
	| resetAndSendCommand    |
	| readOutput             |
	| run                    |
	| substituteParamsInFile |
	| _replaceAll            |
	| __str__                |
	| __repr__               |
	| getResult              |
	+------------------------+
	          .                                                 
	         /_\                                                
	          |                            [ Launcher ]         
	          |                                 .               
	          |                                /_\              
	          |                                 |               
	          |                                 |               
	+----------------------+       +---------------------------+
	| PythonScriptLauncher |       |       ShellLauncher       |
	|----------------------|       |---------------------------|
	| globalVariables      |       | _executable               |
	| localVariables       |       | _prompt                   |
	| queueResult          |       | _exitCommand              |
	| queueOutput          |       | _cleanUpCommand           |
	| result               |       | __out                     |
	| output               |       | __err                     |
	| timeout              |       | __process                 |
	| command              |       | __pid                     |
	| inputParams          |       | __returnCode              |
	|----------------------|       | _outQueue                 |
	| __init__             |       | _errQueue                 |
	| _stdoutIO            |       | _params                   |
	| sendCommand          |       | _result                   |
	| resetAndSendCommand  |       | _resultFile               |
	| _launch              |       | outThread                 |
	| run                  |       | errThread                 |
	| readOutput           |       | timeout                   |
	| setInputParameters   |       | command                   |
	| getResult            |       | inputParams               |
	+----------------------+       |---------------------------|
	                               | __init__                  |
	                               | _launchProcess            |
	                               | _startThreads             |
	                               | _startExecutable          |
	                               | _enqueueOutput            |
	                               | _getOutput                |
	                               | _relaunchIfItIsNotRunning |
	                               | _isSubProcessRunning      |
	                               | sendCommand               |
	                               | resetAndSendCommand       |
	                               | _addTempFileToInputParams |
	                               | _launch                   |
	                               | run                       |
	                               | readOutput                |
	                               | send                      |
	                               | receiveOutput             |
	                               | receiveErrors             |
	                               | communicate               |
	                               | exit                      |
	                               | __del__                   |
	                               | setInputParameters        |
	                               | getResult                 |
	                               +---------------------------+

