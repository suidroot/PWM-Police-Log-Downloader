from subprocess import call
import pdfplumber
import csv
import os

YEAR = '2022'

HOME_DIR = os.environ['HOME']
MEDIA_FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs/Media Logs"

DEBUG = False
CSV_HEADER = ['PD Call#', 'Call Start \nDate & Time', 'Call End \nDate & Time', 'Type of Call', 'Street Address / Location', 'Officer Name']


def pdf_table_extractor(pdf_filename):

    pdf_data = pdfplumber.open(pdf_filename)
    call_list = []
    for pdf_page in pdf_data.pages:
        calls = pdf_page.extract_table()
        del(calls[0])           # remove page header
        call_list.extend(calls)


    if call_list[-1][0] == "Total calls:":
        total_calls = call_list[-1][1] 
        del(call_list[-1])
    else:
        print("Could not get total calls")
        total_calls = 0

    return call_list, int(total_calls)

def write_csv_file(csv_list, csv_file):

    with open(csv_file, 'w') as f:
        write = csv.writer(f)
        write.writerow(CSV_HEADER)
        write.writerows(csv_list)


def get_file_list(YEAR):
    file_list = os.listdir(MEDIA_FILE_LOCATION + '/' + YEAR)
    file_list.sort()
    return file_list

for i in get_file_list(YEAR):
    print(i)

    file_prefix, _ = i.split('.')
    pdf_full_path = MEDIA_FILE_LOCATION + '/' + YEAR + '/' + i
    csv_full_path = MEDIA_FILE_LOCATION + '/' + 'csv/' + YEAR + '/' + file_prefix + '.csv'
 
    call_list, number_calls = pdf_table_extractor(pdf_full_path)
    if len(call_list) != number_calls:
        print(f"PDF Table Parsing Error: Call number mismatch {len(call_list)} != {number_calls}")

    write_csv_file(call_list, csv_full_path)
