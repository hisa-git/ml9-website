#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating cache table..."
python manage.py createcachetable

echo "Starting server..."
exec gunicorn mcl_site.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --worker-tmp-dir /tmp \
    --log-level info \
    --access-logfile - \
    --error-logfile -