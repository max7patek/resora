#!/bin/bash

# Adding Crontabs
#echo Adding Cron Jobs.
#crontab -l
#crontab -e cronfile


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
