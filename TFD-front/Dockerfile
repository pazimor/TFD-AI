FROM node:slim as builder
LABEL authors="pazimor"

WORKDIR /app
COPY . .
RUN npm install -g npm@11.1.0 && npm install -g @angular/cli && npm install
RUN ng build --configuration production

FROM nginx:alpine

COPY --from=builder /app/dist/tfd-front/browser /usr/share/nginx/html
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN chown -R nginx:nginx /usr/share/nginx/html

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80
EXPOSE 443
