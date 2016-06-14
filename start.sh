#!/usr/bin/env bash

C_FORCE_ROOT=1
export C_FORCE_ROOT

service redis-server start
ps -e | grep celery | awk "{print \$1}" | xargs kill

celery -A candidate.celery worker -c 1 -l CRITICAL -q &

echo "scrapy crawl -s RESTART=$1 candidate"

scrapy crawl -s RESTART=$1 candidate
