 #!/bin/bash          

echo "Setting up variables for SMC"

# Edit only this
export SMC_FOLDER=$HOME/smc

export PYTHONPATH=$PYTHONPATH:$SMC_FOLDER/lib/Python

# Creates the FSM
java -jar $SMC_FOLDER/bin/Smc.jar -python -g fsmHandler.sm

