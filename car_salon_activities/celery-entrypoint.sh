#! /bin/bash
set -o errexit
set -o nounset
celery -A config worker --loglevel=INFO --concurrency=10 --hostname worker1@%n