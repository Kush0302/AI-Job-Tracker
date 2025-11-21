#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files (CSS/JS) for production
python manage.py collectstatic --no-input

# Apply database migrations (Update the live database)
python manage.py migrate