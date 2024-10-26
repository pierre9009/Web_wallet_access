# Utilise une image légère de Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Exposer le port que l'application va utiliser
EXPOSE 5000

# Lancer Gunicorn pour démarrer l'application Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "sql_acces:app"]
