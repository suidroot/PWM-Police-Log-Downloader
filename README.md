# PWM-Police-Log-Downloader

This is a tool to download the Police Daily Media Log and Weekly Arrest logs from the City of Portland Maine's Website.

This project requires [Gecko Driver](https://github.com/mozilla/geckodriver) to be installed.

## Approach
The city website dynamically loads the content through javascript, the was a challenge for standard CLI utilities such as curl and wget. The main challenge was to find the URLs for the current day of the week which change on each update by the city. The work flow of this script is as follows:

1. Collect Media log URLs using Selenium Firefox engine
2. Loop through days of the week
    1. Download File 
    2. Collect created date from PDF meta data
    3. Check if file already exists, write file if it does not
    4. Convert PDF tables to CSV
3. Collect Arrest Log URL
    1. Download File 
    2. Collect created date from PDF meta data
    3. Check if file already exists, write file if it does not
    4. Convert PDF tables to CSV