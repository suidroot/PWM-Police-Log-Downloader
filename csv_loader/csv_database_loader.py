#!/usr/bin/which python
import csv
import sqlite_interface as db

FILENAME = '/Volumes/ppd-logs/Media Logs/csv/2023/2023-01-11.csv'
CACHE_CALL_TYPE = {}
CACHE_OFFICER_ID = {}
# Database file
DB_FILE = 'test.db'

class CallClass:
    ''' Data class for each call entry '''
    def __init__(self):
        self.call_id = ''
        self.start = ''
        self.end = ''
        self.call_type = ''
        self.officer_id = ''
        self.address = ''

    def __str__(self):
        return f'''{self.call_id} {self.start} {self.end} \
            {self.call_type} {self.officer_id} {self.address}'''

def csv_file_read(csv_filename):
    ''' Load CSV file parse each row and write entries to a database '''
    with open(csv_filename, newline='') as csvfile:
        call_log_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(call_log_csv, None)
        for row in call_log_csv:
            entry = parse_entry(row)
            write_new_call(entry)


def parse_entry(call_entry):
    ''' Parse individual row from the CSV file '''

    call = CallClass()
    print(call_entry)
    call.call_id = int(call_entry[0])
    call.address = call_entry[4]
    call.start = parse_date_time(call_entry[1])
    call.end = parse_date_time(call_entry[2])

    call_type_id = find_call_type(call_entry[3])
    if call_type_id:
        call.call_type = call_type_id
    else:
        call.call_type = create_new_call_type(call_entry[3])

    officer_id = find_officer(call_entry[5])
    if officer_id:
        call.officer_id = officer_id
    else:
        call.officer_id = create_new_officer(call_entry[5])

    return call

def check_cache(cache, type_text):
    ''' Check in memory cache's for previously seen data '''

    try:
        entry_id = cache[type_text]
    except KeyError:
        entry_id = None

    return entry_id

def parse_date_time(date_text):
    ''' Normalize Date information '''
    return date_text.replace('\n', '')

#
##### Call Type Data #####
def find_call_type(call_text):
    ''' Search for ID of call type '''
    # check runtime cache - CACHE_CALL_TYPE
    call_id = check_cache(CACHE_CALL_TYPE, call_text)
    if not call_id:
        call_id = db.sql_query_type(cnt, call_text)
    # return entry ID or None
    return call_id

def add_call_type_cache(call_id, type_text):
    ''' Add new Call Type to runtime cache '''
    CACHE_CALL_TYPE[type_text] = call_id

def create_new_call_type(call_text):
    ''' Create new call type in the database '''
    db.sql_insert_type(cnt, call_text)
    call_id = find_call_type(call_text)
    # add cache
    add_call_type_cache(call_id, call_text)
    # return ID
    return call_id

#### Officer Data ####
def find_officer(officer_text):
    ''' Search for ID for currently loaded officers '''
    # Split to first and last
    # check runtime cache - CACHE_CALL_TYPE
    officer_id = check_cache(CACHE_OFFICER_ID, officer_text)
    if not officer_id:
        officer_id = db.sql_query_officer(cnt, officer_text)
    # query DB for text
    # return entry ID or None

    return officer_id

def add_officer_cache(officer_id, name_text):
    ''' Add new Officer to runtime cache '''
    CACHE_OFFICER_ID[name_text] = officer_id

def create_new_officer(officer_text):
    ''' Create new officer in the database '''
    lastname, firstname = officer_text.split(', ')
    db.sql_insert_officer(cnt, firstname, lastname, officer_text)
    officer_id = find_officer(officer_text)
    # call DB create function
    add_officer_cache(officer_id, officer_text)

    # return ID
    return officer_id

def write_new_call(call_entry):
    ''' Write to Database '''
    print(call_entry)
    db.sql_insert_call(cnt, call_entry)


####################
####### Main #######
if __name__ == '__main__':
    cnt = db.connect(DB_FILE)
    csv_file_read(FILENAME)
    db.disconnect(cnt)
