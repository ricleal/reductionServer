#!/bin/bash

if [[ $# -lt 1 ]]
then
	echo "Run as: $0 <ILL ASCII RAW file(s) name>" 1>&2;  
	exit 128
fi

raw_filename="$1"

if [ ! -f ${raw_filename} ]; then
    echo "File not found: ${raw_filename}" 1>&2;  
	exit 64
fi

temp_filename=`mktemp -u --tmpdir=/tmp --suffix=.json lamp_XXXXXX`

# THIS WORKS!!!
/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws << EOF > /dev/null 2>&1
json_compile
w = rdopr('${raw_filename}',datp=d)
s = { data_values : w, data_shape : size(w,/DIMENSIONS), data_label :  d.Y_TIT, data_units :  d.Y_TIT, x_axis_shape : size(d.X,/DIMENSIONS), x_axis_values : d.X, x_axis_label : d.X_TIT, x_axis_unit : d.X_TIT }
export_json,s,file="${temp_filename}"
exit
EOF


THIS_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Suppress all output!
python ${THIS_FILE_DIR}/fix_lamp_json.py ${temp_filename} > /dev/null 2>&1

scrict_ret_code=$?

# If exit status from previous command is 0 and temp_filename exists
if [[ ${scrict_ret_code} -eq 0  &&  -f ${temp_filename} ]]
then
    cat ${temp_filename}
fi

rm ${temp_filename}  > /dev/null 2>&1

exit ${scrict_ret_code}





