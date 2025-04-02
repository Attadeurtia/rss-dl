import feedparser
import ytmusicapi
import yt_dlp
import os
import time

# Lire le lien du flux RSS à partir d'une variable d'environnement
RSS_FEED_URL = os.getenv('RSS_FEED_URL', 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLZVH37VAsxC9JIsC5hXX3ku5fgVFBjMTV')  # Valeur par défaut (AURORA — Complete Playlist) au cas où la variable n'est pas définie

# Répertoire de sortie pour les fichiers audio
OUTPUT_DIR = './music'

# Répertoire interne pour le fichier de suivi des articles traités
TRACKING_DIR = './'

# Fichier pour suivre les articles déjà traités
PROCESSED_ARTICLES_FILE = os.path.join(TRACKING_DIR, 'processed_articles.txt')

def get_processed_articles():
    """Récupère la liste des articles déjà traités."""
    if os.path.exists(PROCESSED_ARTICLES_FILE):
        with open(PROCESSED_ARTICLES_FILE, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_processed_article(title):
    """Sauvegarde le titre d'un article traité."""
    with open(PROCESSED_ARTICLES_FILE, 'a') as file:
        file.write(title + '\n')

def search_video(query):
    """Recherche une vidéo sur YouTube Music et retourne son ID."""
    yt = ytmusicapi.YTMusic()
    results = yt.search(query)
    if results:
        return results[0]["videoId"]
    else:
        raise ValueError("Aucune vidéo trouvée pour la requête donnée.")

def download_youtube_audio(video_url):
    """Télécharge l'audio d'une vidéo YouTube au format MP3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def process_rss_feed():
    """Traite le flux RSS pour télécharger l'audio des nouveaux articles."""
    feed = feedparser.parse(RSS_FEED_URL)
    processed_articles = get_processed_articles()

    for entry in feed.entries:
        title = entry.title
        if title not in processed_articles:
            try:
                print(f"Traitement de l'article : {title}")
                video_id = search_video(title)
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                download_youtube_audio(video_url)
                save_processed_article(title)
                print(f"Audio téléchargé avec succès pour : {title}")
            except Exception as e:
                print(f"Erreur lors du traitement de l'article {title} : {e}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TRACKING_DIR, exist_ok=True)
    while True:
        process_rss_feed()
        time.sleep(3 * 60 * 60)  # Attendre 3 heures
