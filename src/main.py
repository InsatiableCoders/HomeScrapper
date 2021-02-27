import os
import configparser

#Upload configuration file
config = configparser.ConfigParser()
config.read('config/system.ini')

#Execute pip update of all dependencies of the project
update_command = config['DEFAULT']['SYSTEM_UPDATE_DEPENDENCIES']
os.system(update_command)