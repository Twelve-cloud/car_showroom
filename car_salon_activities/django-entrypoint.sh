#! /bin/bash
python manage.py migrate
python manage.py runserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT}