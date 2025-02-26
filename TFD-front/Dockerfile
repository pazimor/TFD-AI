# Utiliser l'image officielle de Node.js
FROM node:18-alpine
LABEL authors="pazimor"


# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application Angular dans le conteneur
COPY ./dist/tfd-front /app

# Installer un serveur web simple pour servir Angular
RUN npm install -g serve

# Exposer le port 3000
EXPOSE 3000

# Lancer l'application Angular avec "serve"
CMD ["serve", "-s", "/app", "-l", "3000"]
