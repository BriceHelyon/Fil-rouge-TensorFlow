# Prendre une image de base Node.js
FROM node:18

# Donner le repertoire de travail
WORKDIR /app

# Copier le fichier package.json et package-lock.json
COPY ./package*.json ./

# Installer les dependances JavaScript
RUN npm install

# Copier le reste du code de l'application
COPY . /app

# Construire le projet React
RUN npm run build

# Exposer le port que l'application va utiliser
EXPOSE 3000

# Donner la commande à exécuter
CMD ["npm", "start"]
