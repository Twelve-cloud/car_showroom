#! /bin/bash
pipenv run python manage.py migrate
pipenv run python manage.py runserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT}