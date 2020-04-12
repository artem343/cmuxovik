FROM nginx:1.17.4-alpine

ARG conf_file

RUN rm /etc/nginx/conf.d/default.conf
COPY $conf_file /etc/nginx/conf.d
