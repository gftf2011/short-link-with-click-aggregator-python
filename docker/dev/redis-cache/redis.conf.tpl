bind 0.0.0.0
port 6379
requirepass ${REDIS_CACHE_MASTER_PASSWORD}
aclfile /usr/local/etc/redis/users.acl
protected-mode no

maxmemory ${REDIS_CACHE_MAXMEMORY}
maxmemory-policy allkeys-lru

save ""
appendonly no
