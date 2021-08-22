#!/bin/bash

cd /code

#pip install -r requirements.txt
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput --clear  # Collect static files

# Start Django server
gunicorn tdd_exercise.wsgi:application --bind 0.0.0.0:8801 --workers 3 --reload --log-level debug --access-logfile /tdd-logs/gunicorn.log --forwarded-allow-ips '*'
