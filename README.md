# PWM-Police-Log-Downloader

Downloads Portland, Maine police logs (daily media/dispatch logs and weekly arrest logs) from `portlandmaine.gov`. Uses Selenium to scrape dynamically-loaded PDF URLs, downloads the PDFs, extracts tables with pdfplumber, writes CSVs, and optionally uploads structured data to a REST API.

## Requirements

- [Firefox](https://www.mozilla.org/firefox/) + [Geckodriver](https://github.com/mozilla/geckodriver) (or use Docker — preferred)
- Python 3 + dependencies: `pip install -r requirments.txt`

## Running

```bash
# Local
python3 logdownloaderv2.py

# Docker (handles browser dependencies)
docker run --rm \
  -v /path/to/output:/output \
  usertag/pwmpolicelogdownloader
```

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `FILE_LOCATION` | `~/SynologyDrive/Drive/Documents/Police Logs` | Output directory |
| `LOG_LEVEL` | `WARNING` | Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `ENABLE_DISCORD` | `False` | Enable Discord webhook notifications |
| `DISCORD_PWM_WEBHOOK_URL` | _(required if enabled)_ | Discord webhook URL |
| `ENABLE_UPLOAD` | `False` | Enable CSV upload to REST API |
| `UPLOAD_DISPATCH_URL` | _(required if enabled)_ | API endpoint for dispatch data |
| `UPLOAD_ARREST_URL` | _(required if enabled)_ | API endpoint for arrest data |
| `HEALTHCHECK_URL` | _(optional)_ | URL called via GET on successful completion (e.g. healthchecks.io) |

## Output Directory Structure

The following directories must exist before running (created automatically if missing):

```
[FILE_LOCATION]/Media Logs/[YEAR]/
[FILE_LOCATION]/Media Logs/csv/[YEAR]/
[FILE_LOCATION]/Arrest Logs/[YEAR]/
[FILE_LOCATION]/Arrest Logs/csv/[YEAR]/
```

## Approach

The city website dynamically loads content through JavaScript, which prevents standard tools like `curl` or `wget` from finding the PDF links. Selenium with a headless Firefox browser is used to render the page and extract the current URLs.

Workflow:

1. Collect Media Log URLs using Selenium/Firefox
2. For each day of the week:
   1. Download PDF
   2. Extract creation date from PDF metadata (subtracts 1 day — PDFs are generated the day after the log date)
   3. Write PDF if it doesn't already exist
   4. Extract tables with pdfplumber and write CSV
   5. Optionally upload CSV data to REST API
3. Collect Arrest Log URL using Selenium/Firefox
4. Download, extract, write PDF and CSV (same as above)
5. If `HEALTHCHECK_URL` is set, send a GET request to signal successful completion
