#! /bin/bash
python manage.py migrate --database=master
python manage.py runserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT}