# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Downloads Portland, Maine police logs (daily media/dispatch logs and weekly arrest logs) from `portlandmaine.gov`. Uses Selenium to scrape dynamically-loaded PDF URLs, downloads the PDFs, extracts tables with pdfplumber, writes CSVs, and optionally uploads structured data to a REST API. Discord webhook notifications are supported for monitoring.

## Running the Tool

```bash
# Install dependencies
pip install -r requirments.txt

# Run (requires Firefox + Geckodriver installed locally)
python3 logdownloaderv2.py

# Or via Docker (preferred — handles browser deps)
docker build -t pwmpolicelogdownloader .
docker run --rm -v /path/to/output:/output pwmpolicelogdownloader

# Test run with local API upload endpoint
bash run-test.sh
```

There are no automated tests or linter config. The `test/` directory contains sample PDF/CSV output files for manual verification.

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `FILE_LOCATION` | `~/SynologyDrive/Drive/Documents/Police Logs` | Output directory |
| `LOG_LEVEL` | `WARNING` | Python logging level |
| `ENABLE_DISCORD` | `False` | Enable Discord webhook notifications |
| `DISCORD_PWM_WEBHOOK_URL` | _(required if enabled)_ | Discord webhook URL |
| `ENABLE_UPLOAD` | `False` | Enable CSV upload to REST API |
| `UPLOAD_DISPATCH_URL` | _(required if enabled)_ | API endpoint for dispatch data |
| `UPLOAD_ARREST_URL` | _(required if enabled)_ | API endpoint for arrest data |

## Architecture

**Entry point**: `logdownloaderv2.py` — orchestrates the full pipeline.

**Data flow**:
1. `get_log_urls()` — Selenium/Firefox headless browser loads the dynamically-rendered page, waits `LOAD_TIME_SLEEP` (10s) for JS, then extracts PDF `href` links by link text
2. For each PDF URL: HTTP GET download → PyPDF2 reads `CreationDate` metadata (subtracts 1 day, since PDFs are generated the day after the log date) → file written if it doesn't already exist
3. `pdf_table_extractor()` — pdfplumber iterates pages and extracts tables; validates row count against "Total calls" footer
4. `write_csv_file()` — writes extracted rows with hardcoded header row
5. `upload_data()` — if `ENABLE_UPLOAD`, calls `uploader.py` logic to POST structured JSON to API

**Key modules**:
- [config.py](config.py) — all URLs, paths, feature flags; reads from env vars
- [mylogger.py](mylogger.py) — logger setup with optional Discord handler
- [uploader.py](uploader.py) — parses CSVs and POSTs to REST API; also runnable standalone (`-f filename -m` for dispatch, `-a` for arrest)
- [pdf_parser.py](pdf_parser.py) — legacy bulk PDF-to-CSV converter; not part of main workflow

**Output directory structure** (must exist before running):
```
[FILE_LOCATION]/Media Logs/[YEAR]/
[FILE_LOCATION]/Media Logs/csv/[YEAR]/
[FILE_LOCATION]/Arrest Logs/[YEAR]/
[FILE_LOCATION]/Arrest Logs/csv/[YEAR]/
```

## Docker Notes

- The `/output` path inside the container maps to `FILE_LOCATION`
- SSL verification is disabled (`verify=False`) in HTTP requests — intentional for this site
