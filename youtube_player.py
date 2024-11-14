from pydub import AudioSegment
from pydub.playback import play
import yt_dlp
import os
from threading import Thread
import time


class YouTubePlayer:
    def __init__(self, ffmpeg_path=None):
        self.ffmpeg_path = ffmpeg_path
        if ffmpeg_path:
            os.environ["PATH"] += os.pathsep + ffmpeg_path
        self.currently_playing = False
        self.stop_flag = False
        self.current_file = None  # Stocke le fichier audio en cours

    def search_youtube(self, query):
        """
        Recherche des vidéos YouTube correspondant à une requête.
        Retourne une liste de tuples (titre, URL).
        """
        ydl_opts = {
            'quiet': True,
            'extract_flat': 'videos',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch5:{query}", download=False)
            return [(entry['title'], entry['webpage_url']) for entry in result['entries']]

    def download_audio(self, url, output="audio.mp3"):
        base_name = os.path.splitext(output)[0]  # Supprime toute extension
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{base_name}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        if self.ffmpeg_path:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        self.current_file = f"{base_name}.mp3"  # Assigner le fichier pour nettoyage
        return self.current_file

    def play_audio(self, file_path):
        try:
            self.currently_playing = True
            self.stop_flag = False
            song = AudioSegment.from_file(file_path, format="mp3")

            def playback():
                play(song)
                self.currently_playing = False

            play_thread = Thread(target=playback)
            play_thread.start()

            while self.currently_playing:
                if self.stop_flag:
                    break
                time.sleep(0.1)

            play_thread.join()
            self.cleanup_file()  # Nettoyage après lecture
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture de l'audio : {e}")

    def play_video(self, url):
        try:
            self.stop()  # Stoppe tout audio en cours avant de lancer un nouveau
            audio_file = self.download_audio(url)
            self.play_audio(audio_file)
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture : {e}")

    def stop(self):
        """
        Arrête la lecture en cours et supprime le fichier audio.
        """
        self.stop_flag = True
        print("Arrêt demandé.")
        if self.current_file:
            self.cleanup_file()

    def cleanup_file(self):
        """
        Supprime le fichier audio téléchargé si présent.
        """
        try:
            if self.current_file and os.path.exists(self.current_file):
                os.remove(self.current_file)
                print(f"Fichier {self.current_file} supprimé avec succès.")
            else:
                print(f"Aucun fichier à supprimer ou fichier introuvable : {self.current_file}")
            self.current_file = None
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")
