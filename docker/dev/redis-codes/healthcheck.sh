#!/bin/sh
redis-cli -h 127.0.0.1 -p 6380 --user "${REDIS_CODES_APP_USERNAME}" -a "${REDIS_CODES_APP_PASSWORD}" ping | grep -q PONG
