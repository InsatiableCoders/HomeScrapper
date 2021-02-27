#local dependencies
from scrapper import SpiderManager as sm
from consumer import Consumer as cs

#external dependencies
import os
import configparser
from configparser import ExtendedInterpolation

#Upload configuration file
config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
config.read('config/system.ini')

#Update dependencies (if enabled)
if(config['DEFAULT'].getboolean('UPDATE_DEPENDENCIES')):
    update_command = config['DEFAULT']['SYSTEM_UPDATE_DEPENDENCIES']
    os.system(update_command)

#Fetch spiders to activate
spiders = config['CRAWLER'].get('TO_CRAWL').split('\n')[1:]

#Initiate data Extractor & Consumer
spiderManager = sm.SpiderManager(spiders)
consumer = cs.Consumer()

spiderManager.execute(consumer)