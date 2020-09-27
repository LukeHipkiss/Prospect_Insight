FROM nginx:1.19.0-alpine

COPY ./config /etc/nginx

HEALTHCHECK \
    CMD nc -w5 -z -v 0.0.0.0 80
