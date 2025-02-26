# Utiliser l'image officielle de Node.js
FROM node:18-alpine
LABEL authors="pazimor"

WORKDIR /app
COPY ./dist/tfd-front/browser /app
COPY package.json package-lock.json ./

RUN npm install -g @angular/cli && npm install

EXPOSE 3000
CMD ["serve", "-s", "/app", "-l", "4200"]
