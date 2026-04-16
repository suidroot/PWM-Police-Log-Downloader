from subprocess import call
import os
from logdownloaderv2 import pdf_table_extractor, write_csv_file

YEAR = '2021'
HOME_DIR = os.environ['HOME']
FILE_LOCATION = f"{HOME_DIR}/SynologyDrive/Drive/Documents/Police Logs"
DEBUG = False
MEDIA_LOG=True

if MEDIA_LOG:
    base_file_path = f"{FILE_LOCATION}/Media Logs"
else:
    base_file_path = f"{FILE_LOCATION}/Arrest Logs"

def get_file_list(YEAR):
    file_list = os.listdir(base_file_path + '/' + YEAR)
    file_list.sort()

    return file_list

for i in get_file_list(YEAR):
    print(i)

    file_prefix, _ = i.split('.')
    pdf_new_filename = base_file_path + '/' + YEAR + '/' + i
    csv_filename = base_file_path + '/' + 'csv/' + YEAR + '/' + file_prefix + '.csv'

    if '.pdf' in pdf_new_filename: 
        call_list, number_calls = pdf_table_extractor(pdf_new_filename, media_log=MEDIA_LOG)
        if len(call_list) != number_calls:
            print(f"PDF Table Parsing Error: Call number mismatch {len(call_list)} != {number_calls}")

        write_csv_file(call_list, csv_filename, media_log=MEDIA_LOG)
