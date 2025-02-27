FROM node:slim as builder
LABEL authors="pazimor"

WORKDIR /app
COPY . .
RUN npm install -g npm@11.1.0 && npm install -g @angular/cli && npm install
RUN ng build

FROM nginx:alpine
COPY --from=builder /app/dist/tfd-front/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
