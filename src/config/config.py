'''
Created on Sep 25, 2013

@author: leal

Add this file when needed:

from config.config import options
from config.config import config

'''


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
    return parser

parser = commandLineOptions();
(options, args) = parser.parse_args()


### LOG
import os

LOGGING_CONF=os.path.join(os.path.dirname(__file__),options.log)
 
from logging import config as _config
_config.fileConfig(LOGGING_CONF,disable_existing_loggers=False)


### Configurations
import ConfigParser, os

CONFIG_FILENAME = options.config
config = ConfigParser.ConfigParser()

config.read([CONFIG_FILENAME,
             os.path.join(os.getcwd(),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(os.pardir,CONFIG_FILENAME))]) #..

if __name__ == '__main__':
    print config.get('General','mantid.home')
