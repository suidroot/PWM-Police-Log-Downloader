#!/usr/bin/env python3
''' Configuration for logdownloaderv2.py '''

from os import environ
import logging

MEDIA_LOG_URL = "https://www.portlandmaine.gov/472/Daily-Media-Logs"
ARREST_LOG_URL = "https://www.portlandmaine.gov/471/Crime-in-Portland"

if 'FILE_LOCATION' in environ:
    FILE_LOCATION =  environ['FILE_LOCATION']
else:
    HOME_DIR = environ['HOME']
    FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"

LOAD_TIME_SLEEP = 10
LOGGER_STREAM_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

if 'LOG_LEVEL' in environ:
    if environ['LOG_LEVEL'] == 'INFO':
        LOGGING_LEVEL = logging.INFO
    elif environ['LOG_LEVEL'] == 'WARNING':
        LOGGING_LEVEL = logging.WARNING
    elif environ['LOG_LEVEL'] == 'DEBUG':
        LOGGING_LEVEL = logging.DEBUG
    elif environ['LOG_LEVEL'] == 'ERROR':
        LOGGING_LEVEL = logging.ERROR
    else:
        LOGGING_LEVEL = logging.WARNING
else:
    # Set Log level here if environment variable not set
    LOGGING_LEVEL = logging.WARNING

# Discord Logging
ENABLE_DISCORD = environ.get('ENABLE_DISCORD', '').lower() in ('1', 'true', 'yes')

if ENABLE_DISCORD:
    # set DISCORD_PWM_WEBHOOK_URL shell environment var for webhook URL
    DISCORD_WEBHOOK_URL = environ['DISCORD_PWM_WEBHOOK_URL']
    LOGGER_DISCORD_FORMAT = '%(message)s'
    DISCORD_NAME = "Logdl_bot"

ENABLE_UPLOAD = environ.get('ENABLE_UPLOAD', '').lower() in ('1', 'true', 'yes')

if ENABLE_UPLOAD:
    upload_dispatch_url = environ['UPLOAD_DISPATCH_URL']
    # 'http://ronara.home.lab:8000/add/dispatch/'
    upload_arrest_url = environ['UPLOAD_ARREST_URL'] #'http://ronara.home.lab:8000/add/arrest/'
