#!/bin/sh
set -e

envsubst < /etc/nginx/templates/default.conf.tpl > /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
