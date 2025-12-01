#!/bin/bash

# Exit on error
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn backend.wsgi:application --bind 0.0.0.0:8080 --workers 3
