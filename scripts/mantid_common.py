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
def workspaceToDic(ws):
    res = {}
#     res["type"] = "1d"
#     
#     res["y_axis"] = ws.extractY().shape[1]
#     res["y_axis_data"] = ws.extractY()[0]
#     
#     res["x_axis_size"] = ws.extractX().shape[1]
#     res["x_axis_data"] = ws.extractX()[0]
#     
#     xAxis = ws.getAxis(0)
#     xAxisUnit = xAxis.getUnit()
#     res["x_axis_label"] = xAxisUnit.name()
#     res["x_axis_unit"] = xAxisUnit.label()
#     
#     yAxis = ws.getAxis(1)
#     yAxisUnit = yAxis.getUnit()
#     res["y_axis_label"] = yAxisUnit.name()
#     res["y_axis_unit"] = yAxisUnit.label()


    res["data_values"] = ws.extractY().tolist()
    res["data_shape"] = list(ws.extractY().shape)
    res["data_label"] = ws.YUnitLabel()
    res["data_units"] = ws.YUnit()
    
    res["x_axis_shape"] = [ ws.extractX().shape[1] ]
    res["x_axis_values"] = ws.extractX()[0].tolist()
     
    xAxis = ws.getAxis(0)
    xAxisUnit = xAxis.getUnit()
    res["x_axis_label"] = xAxisUnit.name()
    res["x_axis_unit"] = xAxisUnit.label()
    
    return res
    
def dicToFile(dataDict,filename):
    import json
    with open(filename, 'w') as outfile:
        json.dump(dataDict, outfile)