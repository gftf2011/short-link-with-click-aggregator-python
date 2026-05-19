user ${REDIS_CODES_APP_USERNAME} on >${REDIS_CODES_APP_PASSWORD} resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set +rpush +lpush +lpop ~shortlink:*
