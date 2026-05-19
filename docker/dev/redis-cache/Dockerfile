FROM redis:7-alpine

RUN apk add --no-cache gettext

COPY redis.conf.tpl /usr/local/etc/redis/redis.conf.tpl
COPY users.acl.tpl /usr/local/etc/redis/users.acl.tpl
COPY entrypoint.sh /usr/local/bin/redis-entrypoint.sh
COPY healthcheck.sh /usr/local/bin/redis-healthcheck.sh

RUN chmod +x /usr/local/bin/redis-entrypoint.sh /usr/local/bin/redis-healthcheck.sh

ENTRYPOINT ["/usr/local/bin/redis-entrypoint.sh"]
