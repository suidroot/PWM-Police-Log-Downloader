#!/bin/bash
set -e
chown -R 1000:1000 /output
exec runuser -u ppd -- /opt/PWM-Police-Log-Downloader/logdownloaderv2.py "$@"
