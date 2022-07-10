#!/usr/bin/python3
''' Configuration for logdownloaderv2.py '''

from os import environ

MEDIA_LOG_URL = "https://www.portlandmaine.gov/472/Daily-Media-Logs"
ARREST_LOG_URL = "https://www.portlandmaine.gov/471/Crime-in-Portland"
# Support for Docker
if not environ['FILE_LOCATION']:
    HOME_DIR = environ['HOME']
    FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"
else:
    FILE_LOCATION =  environ['FILE_LOCATION']
DEBUG = False
LOAD_TIME_SLEEP = 10