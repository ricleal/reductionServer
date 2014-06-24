'''
Created on Sep 25, 2013

@author: leal

Add this file when needed:

from config.config import options
from config.config import configParser

'''
import sys
import os
import logging
from logging import config as _config

### Command line options
import optparse
def commandLineOptions():
    '''
    Define command line options
    '''
    parser = optparse.OptionParser()
    parser.add_option('-s', '--server', help='Server host. Default localhost.', default='localhost')
    parser.add_option('-p', '--port',   help='Server port. Default 8080.', type="int", default=8080)
    parser.add_option('-c', '--config', help='Configuration file. Default config.ini.', default='config.ini')
    parser.add_option('-l', '--log',    help='Logging configuration file. Default logging.ini.', default='logging.ini')
    parser.add_option('-i', '--instrument',    help='Intrument to server. If empty looks for instrument name in the config file.', default=None)
    return parser

parser = commandLineOptions();
(options, args) = parser.parse_args()


### File INI configuration
import ConfigParser, os

CONFIG_FILENAME = options.config
configParser = ConfigParser.ConfigParser()

successFullyReadFiles = configParser.read(CONFIG_FILENAME)

if len(successFullyReadFiles) == 0:
    ## CONFIG_FILENAME doesn't exist! Let's read the default file in this folder:
    successFullyReadFiles = configParser.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILENAME))
# ,
#              os.path.join(os.getcwd(),CONFIG_FILENAME),
#              os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILENAME),
#              os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(os.pardir,CONFIG_FILENAME))]) #..

# if not valid file!
if len(successFullyReadFiles) == 0:
    sys.stderr.write('ERROR: The file %s is invalid...\n'%CONFIG_FILENAME)
    sys.exit()

## If the instrument was set through the command line overwrite that from the config.ini

if options.instrument is not None:
    configParser.set("General", "instrument_name",options.instrument)

### File log config
# Log file name will be appended with the instrument name

LOGGING_CONF=os.path.join(os.path.dirname(__file__),options.log)
#_config.fileConfig(LOGGING_CONF,disable_existing_loggers=False)
logFileName = '/tmp/live_%s.log'%configParser.get("General", "instrument_name")
_config.fileConfig(LOGGING_CONF,defaults={'logfilename': logFileName},disable_existing_loggers=False)

# Just to let know the user which config file was parsed
logger = logging.getLogger(__name__)
logger.info("Using config file: %s"%successFullyReadFiles)


logger.info("Server is defined for instrument: %s"%configParser.get("General", "instrument_name"))

## Print parser
for section_name in configParser.sections():
    logger.debug('Section: ' + section_name)
    for name, value in configParser.items(section_name):
        logger.debug('  %s = %s' % (name, value))
