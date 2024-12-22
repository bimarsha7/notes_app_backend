#!/bin/sh

export FLASK_APP='run.py'

# Check for Flask app or Celery worker/beat
if [ "$1" = "backend" ]; then
    # Apply database migrations
    flask db init
    flask db migrate
    flask db upgrade
    # Start the Flask app using Gunicorn
    exec gunicorn --bind 0.0.0.0:5000 --reload "run:app"

elif [ "$1" = "celery-worker" ]; then
    # Start the Celery worker
    exec celery -A app.make_celery worker --loglevel=info

elif [ "$1" = "celery-beat" ]; then
    # Start the Celery beat service for periodic tasks
    exec celery -A app.make_celery beat --loglevel=info
fi
