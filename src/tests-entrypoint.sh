#! /bin/bash
python manage.py migrate --database=${MASTER_DB_NAME}
pytest tests/integration --cov=.