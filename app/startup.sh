#!/bin/sh

python manage.py makemigrations &&
python manage.py migrate &&
python manage.py loaddata tasks/fixtures/initial_data_with_history.json &&
python manage.py collectstatic --noinput &&
pytest &&
gunicorn --bind 0.0.0.0:8000 tasks_manager_project.wsgi:application