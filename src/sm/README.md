State Machine
=============

Prerequisites:
--------------

-	SMC : (http://smc.sourceforge.net/)[http://smc.sourceforge.net/]

**Files**:
- The state machine definition: handler.sm
- The state machine generation: handler_sm.py
- The state machine action code (to be coded!): handler.py

```
export SMC_FOLDER=/home/leal/smc

java -jar $SMC_FOLDER/bin/Smc.jar -python handler.sm

export PYTHONPATH=$PYTHONPATH:SMC_FOLDER/lib/Python

#To test:
python handler.py

```
 