#!/bin/sh

# Démarre Nginx
cp /etc/nginx/conf.d/default.conf.template /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
