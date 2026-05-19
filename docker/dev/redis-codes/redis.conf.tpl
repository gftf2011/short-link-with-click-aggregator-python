bind 0.0.0.0
port 6380

requirepass ${REDIS_CODES_MASTER_PASSWORD}
aclfile /usr/local/etc/redis/users.acl
protected-mode no

maxmemory ${REDIS_CODES_MAXMEMORY}
maxmemory-policy noeviction

save 3600 1
appendonly no
