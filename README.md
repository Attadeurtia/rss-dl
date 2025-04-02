J'ai créé un petit projet Docker qui permet de télécharger automatiquement une playlist YouTube via un flux RSS.

Pour cela, il suffit de copier le lien d'un flux RSS et de choisir le dossier de sortie.

# Histoire

N'utilisant pas d'application de streaming audio, j'ai du mal à suivre les sorties de mes artistes favoris et je rate leurs derniers projets. Pour pallier cela, j'ai trouvé les services [Muspy](https://muspy.com) et [MusicButler](https://www.musicbutler.io) qui permettent de suivre les sorties de ses artistes en flux RSS. Jusqu'à présent, je devais chercher les nouvelles musiques et les ajouter manuellement dans une playlist YouTube.

Maintenant, dès qu'une nouveauté sors sur le flux RSS, le docker le lit, télécharge dans un dossier partagé avec Jellyfin la musique du même nom, ensuite j'ai juste a lancer l’application Jellyfin pour écouter les nouveautés.

Je sais que Lidarr permet de faire la même chose, mais j'écoute des artistes très peu connus qui ne se trouvent que sur YouTube. De plus, mon système est beaucoup plus réactif. Je pense que les deux peuvent fonctionner en complément.

# Fonctionnement

Le projet fonctionne grâce à un script Python exécuté toutes les 3 heures avec les bibliothèques Python *feedparser*, qui permet de lire le flux RSS, *ytmusicapi*, qui permet de faire une recherche sur YouTube Music et de récupérer l'ID d'une vidéo, ainsi que *yt_dlp* (le successeur de YouTube-DL), qui permet de télécharger des playlists YouTube avec de nombreuses options.

Le script vérifie à chaque fois qu'il n'y a pas de doublons grâce à l'URL incluse dans les métadonnées des musiques, puis les télécharge au format *MP3 bestaudio/best 193* dans le dossier choisi.

## Lancer sur docker

pour faire fonctionner le projet :

1.  Télécharger sur GitHub

[github](https://chat.mistral.ai/chat/0ba4418e-5b70-4624-9a5d-2e16924771b3)

1.  Modifier le *docker-compose.yml* pour mettre le chemin désiré et l'url du flux RSS

```yml
version: '3.8'

services:
  youtube-to-mp3:
    build: .
    volumes:
      - ./music:/usr/src/app/music # Remplacez par le chemin de votre choix
    environment:
      - RSS_FEED_URL='https://muspy.com/feed?id=48a1qwnue4jgz9q58ab5jkn8we51qq' # Remplacez par l'URL de votre flux RSS
    restart: always

```

modifier RSS_FEED_URL et ./music

3\. Éxécuter avec la commande

`docker-compose up --build -d`

l'option -d pour l’exécuter en arrière plan

## Lancer simplement avec python

Le scripte python fonctionne également indépendamment, vous pouvez l’exécuter avec la commande : `python3 download_mp3.py`

Pensez juste à changer l'url du flux rss![Capture d’écran 2025-04-02 à 12.55.21.png](:/eb195c79d9c241d48cb5fe957387958a)

**Limites du projet :**

- La musique doit se trouver sur YouTube Music. Je ne sais pas comment YouTube décide si une vidéo sera disponible sur YouTube Music ou non.
- Je ne suis pas satisfait de mon système d'automatisation. J'ai essayé Cron, mais cela fonctionnait mal, et Systemd avec Docker est complexe à mettre en place.
- Cela permet de télécharger des musiques, mais pas l'album complet (sauf si vous avez tous les titres d'un album dans le flux RSS).
- Cela télécharge le premier résultat sur YouTube Music. Bien que dans la majorité des cas, le résultat soit correct, il se peut qu'il télécharge une autre musique ou une version live.