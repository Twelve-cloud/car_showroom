#! /bin/bash
python manage.py migrate --database=${MASTER_DB_NAME}
python manage.py runsslserver ${DJANGO_SERVER_HOST}:${DJANGO_SERVER_PORT} --certificate certs/localhost-dev.crt --key certs/localhost-dev.key