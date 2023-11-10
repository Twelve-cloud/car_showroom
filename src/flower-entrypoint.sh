#! /bin/bash
set -o errexit
set -o nounset
celery -A config flower --loglevel=${FLOWER_LOG_LEVEL} --port=${FLOWER_PORT}