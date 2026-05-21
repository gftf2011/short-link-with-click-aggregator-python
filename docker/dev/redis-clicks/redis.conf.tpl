bind 0.0.0.0
port 6381

requirepass ${REDIS_CLICKS_MASTER_PASSWORD}
aclfile /usr/local/etc/redis/users.acl
protected-mode no

maxmemory ${REDIS_CLICKS_MAXMEMORY}
maxmemory-policy noeviction

save ""
appendonly no
