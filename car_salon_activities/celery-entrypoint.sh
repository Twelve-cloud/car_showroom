#! /bin/bash
set -o errexit
set -o nounset
celery -A car_salon_activities worker --loglevel=INFO --concurrency=10 --hostname worker1@%n