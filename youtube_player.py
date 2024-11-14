from mpv import MPV

class YouTubePlayer:
    def __init__(self):
        # Initialise le lecteur avec youtube-dl activé
        self.player = MPV(ytdl=True, video=False)  # video=False pour audio uniquement

    def play_video(self, url):
        """
        Joue une vidéo ou audio à partir d'un URL YouTube.
        """
        try:
            print(f"Lecture de : {url}")
            self.player.play(url)
            self.player.wait_for_playback()  # Attend la fin de la lecture
        except Exception as e:
            print(f"Erreur lors de la lecture : {e}")

    def stop(self):
        """
        Stoppe la lecture.
        """
        self.player.stop()

# Exemple d'utilisation
if __name__ == "__main__":
    player = YouTubePlayer()
    player.play_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
