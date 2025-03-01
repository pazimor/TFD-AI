#!/bin/sh

# Remplace la variable $API_URL dans config.template.json
envsubst < /usr/share/nginx/html/assets/config.template.json \
        > /usr/share/nginx/html/assets/config.json

# Démarre Nginx
exec nginx -g 'daemon off;'
