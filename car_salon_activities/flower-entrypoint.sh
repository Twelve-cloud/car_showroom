#! /bin/bash
set -o errexit
set -o nounset
celery -A config flower --loglevel=INFO --port=${FLOWER_PORT}