#!/usr/bin/python3
''' Portland Maine Police Log download script '''

# TODO: Directory Management and error handling

from os.path import exists
from tempfile import TemporaryFile
from time import sleep
from datetime import datetime, timedelta
import logging
import csv
import requests
import pdfplumber
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import config

if config.ENABLE_DISCORD:
    # https://pypi.org/project/python-logging-discord-handler/
    from discord_logging.handler import DiscordHandler

DAYS_OF_WEEK = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", \
    "Saturday", "Sunday" ]
MEDIA_CSV_HEADER = ['PD Call#', 'Call Start \nDate & Time', \
    'Call End \nDate & Time', 'Type of Call', 'Street Address / Location', \
    'Officer Name']
ARREST_CSV_HEADER = [ 'Date', 'Arrestee Name', 'Age', 'Home City', 'Charge', \
    'Arrest Type', 'Officer Name', 'Violation Location' ]

MEDIA_LOG_URL = config.MEDIA_LOG_URL
ARREST_LOG_URL = config.ARREST_LOG_URL
DEBUG = config.DEBUG
LOAD_TIME_SLEEP = config.LOAD_TIME_SLEEP
FILE_LOCATION = config.FILE_LOCATION

def setup_logger():
    ''' Set up logging subsystem '''
    logger = logging.getLogger()

    if config.ENABLE_DISCORD:
        discord_handler = DiscordHandler(
            config.DISCORD_NAME,
            config.DISCORD_WEBHOOK_URL )
        discord_format = logging.Formatter(config.LOGGER_DISCORD)
        discord_handler.setFormatter(discord_format)
        logger.addHandler(discord_handler)

    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter(config.LOGGER_STREAM)
    stream_handler.setFormatter(stream_format)

    # Add the handlers to the Logger
    logger.addHandler(stream_handler)
    logger.setLevel(config.LOGGING_LEVEL)

    return logger

def create_firefox_object(headless=True):
    ''' Create Firefox Object with option to disable headless mode '''

    if headless:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()

    return driver

def get_arrest_log_url(headless=True):
    ''' Search for the URL of the Arrest Logs in webpage '''

    driver = create_firefox_object(headless)
    driver.get(ARREST_LOG_URL)
    sleep(LOAD_TIME_SLEEP)

    link_element = driver.find_element(By.LINK_TEXT, "View Weekly Arrest Log")
    url_data = link_element.get_attribute('href')
    driver.quit()

    return url_data

def get_media_log_urls(days):
    ''' Iterate over list of days of the week to find the URLs of the daily media logs'''
    url_data = {}

    driver = create_firefox_object()
    driver.get(MEDIA_LOG_URL)
    sleep(LOAD_TIME_SLEEP)

    for day in days:
        try:
            link_element = driver.find_element(By.LINK_TEXT, day)
            day_url = link_element.get_attribute('href')
            url_data[day] = day_url
        except Exception as exception_info:
            logger.error("The error raised is: %s", exception_info)

        logger.debug("%s: %s", day, day_url)

    driver.quit()

    return url_data

def download_content(url):
    ''' Download PDF Data '''

    response = requests.get(url)
    return response.status_code, response.content

def get_pdf_meta_data(data):
    ''' Find the Create time of the PDF file and parse to datetime subtracting 1 day '''
    meta_data = {}

    temp_file_pointer = TemporaryFile()
    temp_file_pointer.write(data)
    temp_file_pointer.seek(0)

    reader = PdfReader(temp_file_pointer)
    # "D:20220621061003-04'00'"
    pdf_date = reader.getDocumentInfo()['/CreationDate']
    meta_data['pdf_date'] = datetime.strptime(pdf_date, "D:%Y%m%d%H%M%S-04'00'") - timedelta(1)
    temp_file_pointer.close()

    return meta_data

def pdf_table_extractor(pdf_filename, media_log=True):
    ''' Extract Table data from PDF data '''

    pdf_data = pdfplumber.open(pdf_filename)
    call_list = []
    for pdf_page in pdf_data.pages:
        calls = pdf_page.extract_table()
        del calls[0]            # remove page header
        call_list.extend(calls)

    # extract Total calls from PDF if unable to find print error
    if call_list[-1][0] == "Total calls:":
        total_calls = call_list[-1][1]
        del call_list[-1]
    elif "Total Calls For PD Service Reported:" in call_list[-1][0]:
        total_calls = call_list[-1][0].split(":")[1].lstrip(" ")
        del call_list[-1]
    elif not media_log:
        try:
            total_calls = int(call_list[-1][0])
            del call_list[-1]
        except ValueError:
            logger.error("Could not get total calls")
            total_calls = 0
    else:
        logger.error("Could not get total calls")
        total_calls = 0

    return call_list, int(total_calls)

def write_csv_file(csv_list, csv_file, media_log=True):
    ''' Write list to CSV file '''

    if media_log:
        csv_header = MEDIA_CSV_HEADER
    else:
        csv_header = ARREST_CSV_HEADER

    with open(csv_file, 'w') as csv_file_handle:
        write = csv.writer(csv_file_handle)
        write.writerow(csv_header)
        write.writerows(csv_list)

def write_pdf_and_csv(meta_data, data, media_log=True):
    ''' Write the PDF file and CVS version of the files to disk '''

    # subtract 1 day
    date_str =  meta_data['pdf_date'].strftime("%Y-%m-%d")
    year_str =  meta_data['pdf_date'].strftime("%Y")
    if media_log:
        pdf_new_filename = f"{FILE_LOCATION}/Media Logs/{year_str}/{date_str}.pdf"
        csv_filename = f"{FILE_LOCATION}/Media Logs/csv/{year_str}/{date_str}.csv"
    else:
        pdf_new_filename = f"{FILE_LOCATION}/Arrest Logs/{year_str}/arrestlog_{date_str}.pdf"
        csv_filename = f"{FILE_LOCATION}/Arrest Logs/csv/{year_str}/arrestlog_{date_str}.csv"

    if not exists(pdf_new_filename):
        logger.warning("writing %s to %s", date_str, pdf_new_filename)

        with open(pdf_new_filename,'wb') as pdf_file:
            pdf_file.write(data)
    else:
        logger.info("Skipping writing %s exists at %s", date_str, pdf_new_filename)

    if not exists(csv_filename):
        logger.warning("Creating csv of %s to %s", date_str, csv_filename)

        call_list, number_calls = pdf_table_extractor(pdf_new_filename, media_log=media_log)
        if len(call_list) != number_calls:
            logger.error("PDF Table Parsing Error: Call \
                number mismatch %d != %d", len(call_list), number_calls)
        write_csv_file(call_list, csv_filename, media_log=media_log)
    else:
        logger.info("Skipping csv of %s exists at %s", date_str, csv_filename)

def main():
    ''' Main function '''

    logger.warning("Getting Media Log URLs")
    url_data = get_media_log_urls(DAYS_OF_WEEK)

    for day in DAYS_OF_WEEK:
        logger.info("Downloading %s", day)
        logger.debug("Downloading %s : %s", day, url_data[day])
        status_code, content = download_content(url_data[day])

        if status_code == 200:
            meta_data = get_pdf_meta_data(content)
            date = meta_data['pdf_date'].strftime("%Y-%m-%d")
            logger.debug('PDF date: %s', date)
            write_pdf_and_csv(meta_data, content)
        else:
            logger.error("**** %s file not found on server: %s error ***", day, status_code)

    logger.warning("Starting Arrest Log")
    status_code, content = download_content(get_arrest_log_url())

    if status_code == 200:
        meta_data = get_pdf_meta_data(content)
        write_pdf_and_csv(meta_data, content, media_log=False)
    else:
        logger.error("%s file not found", day)

if __name__ == '__main__':
    logger = setup_logger()
    main()
