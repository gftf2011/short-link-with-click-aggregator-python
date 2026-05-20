#!/bin/sh
redis-cli -h 127.0.0.1 -p 6381 --user "${REDIS_CLICKS_APP_USERNAME}" -a "${REDIS_CLICKS_APP_PASSWORD}" ping | grep -q PONG
