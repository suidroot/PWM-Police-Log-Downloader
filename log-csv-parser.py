#!/usr/bin/python

import csv
import os
from datetime import datetime

HOME_DIR = os.environ['HOME']
FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"
year_str = '2022'
date_str = '2022-06-23'
csv_filename = f"{FILE_LOCATION}/Media Logs/csv/{year_str}/{date_str}.csv"


def validate_date(date_text: str) -> bool:
    ''' Validate Date is correct format '''

    return_val = True

    try:
        datetime.strptime(date_text, '%m/%d/%Y')
    except ValueError:
        return_val = False

    return return_val

def validate_time(date_text: str) -> bool:
    ''' Validate Time is correct format '''

    return_val = True

    try:
        # 12:13 AM
        datetime.strptime(date_text, '%I:%M %p')
    except ValueError:
        return_val = False

    return return_val

all_entries = []
total_calls = 0

with open(csv_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    group_counter = 0
    isheader = False
    issingleline = False
    allcount = 0

    for row in csv_reader:

        print(f'{allcount} {group_counter} raw row: {row}')

        if row[0] == 'Total calls:':
            total_calls = int(row[1])
        # 1 line header
        elif row[0] == 'PD Call#' and row[1] == 'Call Start\nDate & Time':
            print('singhead')
            isheader = True
            issingleline = True
        elif row[0] != '' and row[1] != '':
            call_number = row[0]
            start_date, start_time = row[1].split('\n')
            stop_date, stop_time = row[2].split('\n')
            call_reason = row[3]
            call_address = row[4]
            call_officer = row[5]
            group_counter += 1
            issingleline = True
        # 3 line header
        elif row[0] == '' and row[1] == 'Call Start':
            print('head1')
            group_counter += 1
            isheader = True
            pass 
        elif row[0] == 'PD Call#' and row[1] == '':
            print('head2')
            group_counter += 1
            isheader = True
            pass
        elif row[0] == '' and row[1] == 'Date & Time':
            print('head3')
            group_counter += 1
            isheader = True
            pass
        elif row[0] == '' and validate_date(row[1]):
            print('line1')
            # ['', '06/22/2022', '06/22/2022', '', '', '']
            start_date = row[1]
            stop_date = row[2]
            group_counter += 1
        elif row[0] != '' and group_counter < 2:
            print('line2')
            # ['2022030449', '', '', 'Indecent Exposure', '10 Dana St', 'McIlwaine, Kyle']
            call_number = row[0]
            call_reason = row[3]
            call_address = row[4]
            call_officer = row[5]
            group_counter += 1
        elif row[0] == '' and validate_time(row[1]):
            print('line3')
            # ['', '06:08 PM', '06:17 PM', '', '', '']
            start_time = row[1]
            stop_time = row[2]
            group_counter += 1
    
        if (group_counter == 3 and isheader) or (issingleline and isheader):
            print('header match')
            group_counter = 0
            isheader = False
            if issingleline:
                issingleline = False

        elif (issingleline or group_counter == 3) and not isheader:
            entry = {
                'call_number' : call_number,
                'start_date' : start_date,
                'start_time' : start_time,
                'stop_date' : stop_date,
                'stop_time' : stop_time,
                'call_reason' : call_reason,
                'call_address' : call_address,
                'call_officer' : call_officer
            }
            if issingleline:
                issingleline = False

            group_counter = 0

            print(f'entry {entry}')
            all_entries.append(entry)

            entry = {}
            
        allcount += 1


print(len(all_entries))
print(total_calls)


