#!/bin/sh
set -e

envsubst < /usr/local/etc/redis/redis.conf.tpl > /usr/local/etc/redis/redis.conf
envsubst < /usr/local/etc/redis/users.acl.tpl > /usr/local/etc/redis/users.acl

exec redis-server /usr/local/etc/redis/redis.conf
