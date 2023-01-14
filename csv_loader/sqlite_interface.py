#!/usr/bin/which python
''' SQLite Database interface wrappers '''

import sqlite3

def connect(db_file):
    ''' Load SQLite file '''
    return sqlite3.connect(db_file)

def disconnect(cnt):
    ''' Close SQLite file '''
    cnt.close()

def execute_command(cnt, command):
    ''' Execute SQLite SQL phrases '''
    # TODO: Error handling
    return cnt.execute(command)

## SQL call wrappers
def sql_insert_call(cnt, call):
    ''' Wrapper to generate and execute insert call entry '''
    execute_command(cnt, generate_insert(call))
    cnt.commit()

def sql_insert_officer(cnt, firstname, lastname, display_text):
    ''' Wrapper to generate and execute insert new officer entry '''
    execute_command(cnt, \
        generate_officer_insert(firstname, lastname, display_text))
    cnt.commit()

def sql_insert_type(cnt, display_text):
    ''' Wrapper to generate and execute insert new call_type entry '''
    execute_command(cnt, \
        generate_type_insert(display_text))
    cnt.commit()

def sql_query_officer(cnt, display_text):
    ''' Query database for Officer display name and return row ID '''
    officer_id = None

    results = execute_command(cnt, \
        generate_id_query('officers', display_text))

    for i in results:
        officer_id = i[0]

    return officer_id

def sql_query_type(cnt, display_text):
    ''' Query database for call_type display name and return row ID '''
    type_id = None

    results = execute_command(cnt, \
        generate_id_query('call_types', display_text))

    for i in results:
        type_id = i[0]

    return type_id

## Generate SQL query strings
def generate_insert(call):
    ''' Generate SQL syntax to insert police call to database'''

    table_name = 'pwm_police_calls'

    query =  f'''INSERT INTO {table_name} (
        call_number,
        call_start,
        call_stop,
        officer,
        call_type,
        call_address
    ) VALUES (
        {call.call_id},
        "{call.start}",
        "{call.end}",
        {call.officer_id},
        {call.call_type},
        "{call.address}"
    );'''
        # STRFTIME("%m/%d/%Y %I:%M %p", "{call.start}"),
        # STRFTIME("%m/%d/%Y %I:%M %p", "{call.end}"),

    # print(query)

    return query

def generate_id_query(table, text):
    ''' Generate SQL syntax to find ID of from resource databases '''

    query = f'''SELECT ID FROM {table} WHERE display_text = "{text}";'''
    # print(query)
    return query

def generate_officer_insert(firstname, lastname, display_text):
    ''' Generate SQL syntax to INSERT new Officer '''

    return f'''INSERT INTO officers (firstname, lastname, display_text)
    VALUES ("{firstname}", "{lastname}", "{display_text}");'''

def generate_type_insert(display_text):
    ''' Generate SQL syntax to INSERT new call_type '''

    return f'''INSERT INTO call_types (display_text)
    VALUES ("{display_text}");'''