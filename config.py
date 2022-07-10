#!/usr/bin/python3
''' Configuration for logdownloaderv2.py '''

from os import environ

HOME_DIR = environ['HOME']
MEDIA_LOG_URL = "https://www.portlandmaine.gov/472/Daily-Media-Logs"
ARREST_LOG_URL = "https://www.portlandmaine.gov/471/Crime-in-Portland"
FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"
DEBUG = False
LOAD_TIME_SLEEP = 10