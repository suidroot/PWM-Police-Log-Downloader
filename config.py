#!/usr/bin/python3
''' Configuration for logdownloaderv2.py '''

from os import environ
import logging

MEDIA_LOG_URL = "https://www.portlandmaine.gov/472/Daily-Media-Logs"
ARREST_LOG_URL = "https://www.portlandmaine.gov/471/Crime-in-Portland"
# Support for Docker
try:
    FILE_LOCATION =  environ['FILE_LOCATION']
except KeyError:
    HOME_DIR = environ['HOME']
    FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"

DEBUG = False
LOAD_TIME_SLEEP = 10
LOGGER_STREAM = '%(asctime)s - %(levelname)s - %(message)s'
LOGGING_LEVEL = logging.INFO

# Discord Logging
ENABLE_DISCORD = True
# set shell environment var for webhook URL
DISCORD_WEBHOOK_URL = environ['DISCORD_PWM_WEBHOOK_URL']
LOGGER_DISCORD = '%(message)s'
DISCORD_NAME = "Logdl_bot"