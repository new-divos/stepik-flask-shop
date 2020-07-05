FROM nginx:1.17-alpine

ENV STATIC_ROOT /www
VOLUME ["${STATIC_ROOT}"]

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d