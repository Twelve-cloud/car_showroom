#! /bin/bash
set -o errexit
set -o nounset
celery -A config worker --loglevel=${WORKER_LOG_LEVEL} --concurrency=10 --hostname worker1@%n