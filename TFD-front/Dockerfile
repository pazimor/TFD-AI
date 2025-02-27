FROM node:18-alpine as builder
LABEL authors="pazimor"
WORKDIR /app
COPY package*.json ./
RUN npm install -g @angular/cli && npm install
COPY . .
RUN ng build

FROM nginx:alpine
COPY --from=builder /app/dist/tfd-front/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
