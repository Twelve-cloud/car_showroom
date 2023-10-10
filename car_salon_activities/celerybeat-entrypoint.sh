#! /bin/bash
set -o errexit
set -o nounset
celery -A car_salon_activities beat --loglevel=INFO