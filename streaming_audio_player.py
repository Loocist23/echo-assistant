import os
import yt_dlp
from pydub import AudioSegment
import pyaudio
import wave
import time
from threading import Thread


class StreamingAudioPlayer:
    def __init__(self, ffmpeg_path=None):
        self.ffmpeg_path = ffmpeg_path
        if ffmpeg_path:
            os.environ["PATH"] += os.pathsep + ffmpeg_path
        self.current_file = None
        self.stop_flag = False
        self.volume_db = -15  # Volume initial (-15 dB)
        self.audio_stream = None  # Ajout pour suivre l'état du flux

    def is_playing(self):
        """Vérifie si l'audio est en cours de lecture."""
        return self.audio_stream and self.audio_stream.is_active()

    def search_youtube(self, query):
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
        AudioSegment.from_mp3(mp3_file).export(self.current_file, format="wav")
        os.remove(mp3_file)
        return self.current_file

    def play_audio(self, file_path):
        wf = wave.open(file_path, 'rb')
        p = pyaudio.PyAudio()
        self.stop_flag = False

        self.audio_stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                   channels=wf.getnchannels(),
                                   rate=wf.getframerate(),
                                   output=True)

        print("Lecture de l'audio...")
        while not self.stop_flag:
            data = wf.readframes(1024)
            if not data:
                break
            self.audio_stream.write(self._apply_volume(data), num_frames=1024)

        self.audio_stream.stop_stream()
        self.audio_stream.close()
        p.terminate()
        wf.close()
        self.cleanup_file()

    def _apply_volume(self, data):
        """Applique un gain au flux audio."""
        audio = AudioSegment(data, sample_width=2, frame_rate=44100, channels=2)
        audio = audio + self.volume_db
        return audio.raw_data

    def play_video(self, url):
        try:
            self.stop()
            audio_file = self.download_audio(url)
            Thread(target=self.play_audio, args=(audio_file,)).start()
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture : {e}")

    def increase_volume(self):
        self.volume_db = min(0, self.volume_db + 5)
        print(f"Volume augmenté : {self.volume_db} dB")

    def decrease_volume(self):
        self.volume_db = max(-50, self.volume_db - 5)
        print(f"Volume diminué : {self.volume_db} dB")

    def stop(self):
        self.stop_flag = True

    def cleanup_file(self):
        if self.current_file and os.path.exists(self.current_file):
            os.remove(self.current_file)
            print(f"Fichier {self.current_file} supprimé.")
        self.current_file = None
