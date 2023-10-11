#! /bin/bash
set -o errexit
set -o nounset
celery -A car_salon_activities flower --loglevel=INFO --port=${FLOWER_PORT}