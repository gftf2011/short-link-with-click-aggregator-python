user ${REDIS_CACHE_APP_USERNAME} on >${REDIS_CACHE_APP_PASSWORD} resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set ~*
