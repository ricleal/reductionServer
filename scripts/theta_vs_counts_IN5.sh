#!/bin/bash

if [[ $# -lt 1 ]]
then
	echo "Run as: $0 <Nexus file name>" 1>&2;  
	exit 128
fi

nexus_filename="$1"

if [ ! -f ${nexus_filename} ]; then
    echo "File not found: ${nexus_filename}" 1>&2;  
	exit 64
fi

temp_filename=`mktemp -u --tmpdir=/tmp --suffix=.json mantid_XXXXXX`

THIS_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# Suppress all output!
python ${THIS_FILE_DIR}/theta_vs_counts_IN5.py ${nexus_filename} ${temp_filename} > /dev/null 2>&1

scrict_ret_code=$?

# If exit status from previous command is 0 and temp_filename exists
if [[ ${scrict_ret_code} -eq 0  &&  -f ${temp_filename} ]]
then
    cat ${temp_filename}
fi

rm ${temp_filename}  > /dev/null 2>&1

exit ${scrict_ret_code}
