#! /bin/bash
python manage.py makemigrations
python manage.py migrate --database=master
python manage.py runserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT}