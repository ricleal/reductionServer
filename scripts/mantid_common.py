### File INI configuration
import ConfigParser, os

CONFIG_FILENAME = 'config.ini'
configParser = ConfigParser.ConfigParser()

configParser.read([CONFIG_FILENAME,
             os.path.join(os.getcwd(),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(os.pardir,CONFIG_FILENAME))]) #..

### Mantid imports

import sys
sys.path.append(configParser.get('Mantid','bin_folder'))

from mantid.simpleapi import *

### Usefull functions
def exportWs1DToDicFile(ws,outfilename):
    res = {}
    res["type"] = "1d"
    res["data_size"]=ws.extractY().shape[1]
    res["data"]=ws.extractY()[0]
    
    res["x_axis_size"]=ws.extractX().shape[1]
    res["x_axis_data"]=ws.extractX()[0]
    res["x_axis_label"]=ws.YUnitLabel()
    res["x_axis_unit"]=ws.YUnit()
    
    
    return res
    