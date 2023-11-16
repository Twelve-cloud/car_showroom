#! /bin/bash
if [[ -z "${KUBERNETES}" ]]; then
  python manage.py migrate
else
  python manage.py migrate --database=${MASTER_DB_NAME}
fi