#! /bin/bash
python manage.py migrate --database=${MASTER_DB_NAME}
gunicorn config.wsgi:application --workers=8 --certfile=certs/localhost-prod.crt --keyfile=certs/localhost-prod.key --bind ${DJANGO_GUNICORN_HOST}:${DJANGO_GUNICORN_PORT}