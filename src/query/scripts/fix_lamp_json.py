#!/usr/bin/python

'''
Created on Nov, 2013

@author: leal

Modifies imput file

'''

import json

def fixPlot1D(jsonData):

    d = json.loads(jsonData)
    
    # convert keys to lowercase
    d = dict((k.lower(), v) for k, v in d.iteritems())
    
    # Because for 1D we need data shape as: "data_shape": [1, 135]
    if len(d["data_shape"]) == 1:
        d["data_shape"].insert(0,1) # put 1 at the header! = [1,d["data_shape"]]
    #d["x_axis_shape"] = [d["x_axis_shape"]]
    
    # outputs the dic correscted
    
    return d
