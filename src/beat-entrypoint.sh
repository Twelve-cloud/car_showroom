#! /bin/bash
set -o errexit
set -o nounset
celery -A config beat --loglevel=${BEAT_LOG_LEVEL}