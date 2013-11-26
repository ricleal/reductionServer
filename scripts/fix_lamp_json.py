#!/usr/bin/python

'''
Created on Nov, 2013

@author: leal

Modifies imput file

'''

import json
import sys

if len(sys.argv) <= 1:
    sys.exit(-2)

# read stdin
#data = sys.stdin.read()
data = open(sys.argv[1],'r')
d = json.loads(data.read())
data.close()

# convert keys to lowercase
d = dict((k.lower(), v) for k, v in d.iteritems())

# Because for 1D we need data shape as: "data_shape": [1, 135]
if len(d["data_shape"]) == 1:
     d["data_shape"].insert(0,1) # put 1 at the header! = [1,d["data_shape"]]
#d["x_axis_shape"] = [d["x_axis_shape"]]

# outputs the dic correscted
data = open(sys.argv[1],'w')
data.write(json.dumps(d))
data.close()