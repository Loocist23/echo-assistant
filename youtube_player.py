from pydub import AudioSegment
import os
import yt_dlp
import simpleaudio as sa
import time


class YouTubePlayer:
    def __init__(self, ffmpeg_path=None):
        self.ffmpeg_path = ffmpeg_path
        if ffmpeg_path:
            os.environ["PATH"] += os.pathsep + ffmpeg_path
        self.current_file = None
        self.stop_flag = False
        self.play_obj = None

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
        base_name = os.path.splitext(output)[0]
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{base_name}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        mp3_file = f"{base_name}.mp3"
        self.current_file = f"{base_name}.wav"

        # Convert MP3 to WAV
        AudioSegment.from_mp3(mp3_file).export(self.current_file, format="wav")
        os.remove(mp3_file)  # Supprime le fichier MP3 après conversion
        return self.current_file

    def play_audio(self, file_path):
        try:
            self.stop_flag = False
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            self.play_obj = wave_obj.play()

            print("Lecture de l'audio...")

            while self.play_obj.is_playing():
                if self.stop_flag:
                    self.play_obj.stop()
                    print("Arrêt de la lecture demandé.")
                    break
                time.sleep(0.1)

            self.cleanup_file()  # Nettoyage après lecture
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture de l'audio : {e}")

    def play_video(self, url):
        try:
            self.stop()  # Arrête tout ce qui joue actuellement
            audio_file = self.download_audio(url)
            self.play_audio(audio_file)
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture : {e}")

    def stop(self):
        self.stop_flag = True
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            print("Lecture arrêtée.")

    def cleanup_file(self):
        if self.current_file and os.path.exists(self.current_file):
            os.remove(self.current_file)
            print(f"Fichier {self.current_file} supprimé.")
        self.current_file = None
