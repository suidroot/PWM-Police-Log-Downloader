#!/bin/bash
set -e
chown -R ppd:ppd /output
exec runuser -u ppd -- /opt/PWM-Police-Log-Downloader/logdownloaderv2.py "$@"
