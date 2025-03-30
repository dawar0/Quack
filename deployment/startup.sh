#!/bin/bash
set -e

# Start Nginx in the background
service nginx start

# Run database migrations
flask db upgrade

# Start the Flask application with gunicorn
exec gunicorn --bind 0.0.0.0:5000 'app:create_app()'