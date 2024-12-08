# Prendre une image de base Python
FROM python:3.12.5-slim

# Donner le repertoire de travail
WORKDIR /app

# Copier le fichier des dependances python
COPY ./requirements.txt ./

# Installer les dependances Python
RUN pip install --no-cache-dir -r ./requirements.txt

# Copier le reste du code de l'application
COPY . /app

# Exposer le port que l'application va utiliser
EXPOSE 8000

# Donner la commande a lancer
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
