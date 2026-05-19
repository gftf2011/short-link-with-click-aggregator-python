FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="Gabriel Ferrari Tarallo Ferraz"

USER root

RUN apk add --no-cache gettext

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf.tpl /etc/nginx/templates/default.conf.tpl
COPY uvicorn_proxy.conf /etc/nginx/uvicorn_proxy.conf
COPY run.sh /run.sh

ENV LISTEN_PORT=8080 \
    APP_HOST=api \
    APP_PORT=8000

RUN chmod +x /run.sh \
    && chown nginx:nginx /etc/nginx/nginx.conf \
    && chown nginx:nginx /etc/nginx/uvicorn_proxy.conf \
    && touch /etc/nginx/conf.d/default.conf \
    && chown nginx:nginx /etc/nginx/conf.d/default.conf

USER nginx

EXPOSE 8080

CMD ["/run.sh"]
