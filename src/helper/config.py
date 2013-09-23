'''
Created on Sep 23, 2013

@author: leal
'''


import ConfigParser, os

CONFIG_FILENAME = 'config.ini'

config = ConfigParser.ConfigParser()
config.read([CONFIG_FILENAME,
             os.path.join(os.getcwd(),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),CONFIG_FILENAME),
             os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(os.pardir,CONFIG_FILENAME))]) #..


if __name__ == '__main__':
    print config.get('General','mantid.home')