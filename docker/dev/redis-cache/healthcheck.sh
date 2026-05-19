#!/bin/sh
redis-cli -h 127.0.0.1 --user "${REDIS_CACHE_APP_USERNAME}" -a "${REDIS_CACHE_APP_PASSWORD}" ping | grep -q PONG
