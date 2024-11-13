#!/bin/sh
# bash file with your commands

python manage.py runserver 0.0.0.0:8000 &&
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py loaddata tasks/fixtures/initial_data_with_history.json