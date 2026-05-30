upstream uvicorn_backend {
    server ${APP_HOST}:${APP_PORT};
    keepalive 256;
}

server {
    listen ${LISTEN_PORT};

    client_max_body_size 1M;

    location / {
        include /etc/nginx/uvicorn_proxy.conf;
        proxy_pass http://uvicorn_backend;
        proxy_redirect off;
        proxy_connect_timeout 5s;
        proxy_send_timeout 5s;
        proxy_read_timeout 5s;
    }
}
