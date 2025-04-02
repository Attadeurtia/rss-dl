# Utiliser une image de base Alpine avec Python 3.9
FROM python:alpine

# Installer les dépendances nécessaires
RUN apk add --no-cache \
    ffmpeg \
    wget \
    bash \
    && pip install ytmusicapi yt-dlp feedparser

# Copier le script Python dans le conteneur
COPY download_mp3.py /usr/src/app/download_mp3.py

# Définir le répertoire de travail et créer les répertoires nécessaires
WORKDIR /usr/src/app
RUN mkdir -p ./music

# Démarrer le script Python
CMD ["python3", "/usr/src/app/download_mp3.py"]
