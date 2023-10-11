#! /bin/bash
python manage.py migrate --database=master
python manage.py runsslserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT} --certificate localhost.crt --key localhost.key