#!/usr/bin/python

'''
Created on Sep 25, 2013

@author: leal
'''


import sys
import errno

# if len(sys.argv) != 3 :
#     sys.stderr.write("Run as %s <Nexus file path> <output json file>\n"%(sys.argv[0]))
#     sys.exit(errno.EINVAL)




# import everything
from query.scripts.mantid_common import *

datafile = '%{data_file_full_path}'

maskfile = configParser.get('Mantid','in5_mask_file')

# ## Redirect STDOUT STDERR
# import sys, os, logging
# sys.stdout = os.devnull
# sys.stderr = os.devnull
# logger = logging.getLogger()
# logger.disabled = True


# load data
Load(Filename=datafile,OutputWorkspace='Data')
# Load Mask
LoadMask(Instrument='IN5',InputFile=maskfile ,OutputWorkspace='IN5_Mask')
# Apply mask to the detector - data
MaskDetectors(Workspace='Data',MaskedWorkspace='IN5_Mask')
# Show Instrument -> Cylindrical Y

#viewDetector('Data')

ConvertUnits(InputWorkspace='Data',OutputWorkspace='Data_DeltaE',Target='DeltaE',EMode='Direct')
Rebin(InputWorkspace='Data_DeltaE',OutputWorkspace='Data_DeltaE_Rebined',Params='-40,0.1,2',PreserveEvents='0')
# put the theta rings (detector ids) in a temp file
GenerateGroupingPowder(InputWorkspace='Data_DeltaE_Rebined',AngleStep='1',GroupingFilename='/tmp/group.xml')
# group the detector in rings => merge data!
GroupDetectors(InputWorkspace='Data_DeltaE_Rebined',OutputWorkspace='Data_grouped',MapFile=r'/tmp/group.xml')

#viewDetector('Data_grouped')

ConvertSpectrumAxis(InputWorkspace='Data_grouped',OutputWorkspace='Data_grouped_2theta',Target='theta')
# Do a Color Fill Plot
Integration(InputWorkspace='Data_grouped_2theta',OutputWorkspace='Data_grouped_2theta_I')
t = Transpose(InputWorkspace='Data_grouped_2theta_I',OutputWorkspace='Data_grouped_2theta_I_T')

# # Do a Plot of the unique Spectrum
# p = plotSpectrum(t,0)
# l = p.activeLayer()
# # Retitle the y-axis
# l.setAxisTitle(Layer.Bottom, "Theta")

result = workspaceToDic(t)
