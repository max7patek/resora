#!/bin/bash

echo Starting Cron Jobs.
crontab -l
cron

echo Starting Gunicorn.
exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --forwarded-allow-ips="*"
