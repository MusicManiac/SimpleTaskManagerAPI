#!/bin/sh

python manage.py makemigrations &&
python manage.py migrate &&
python manage.py loaddata tasks/fixtures/initial_data_with_history.json &&
echo 'Open http://127.0.0.1:8000/api/ or run cURL commands from terminal' &&
python manage.py runserver 0.0.0.0:8000
