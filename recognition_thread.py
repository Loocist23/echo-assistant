from PyQt5.QtCore import QThread, pyqtSignal
from voice_recognition import VoiceRecognition
from youtube_player import YouTubePlayer
from intent_handler import IntentHandler
from threading import Thread, Event

class RecognitionThread(QThread):
    result_signal = pyqtSignal(str)
    audio_feedback_signal = pyqtSignal(str)

    def __init__(self, output_device):
        super().__init__()
        self.voice_recognition = VoiceRecognition()
        self.youtube_player = YouTubePlayer()
        self.intent_handler = IntentHandler()
        self.output_device = output_device
        self.running = True
        self.stop_event = Event()  # Event pour signaler un arrêt propre au player

    def run(self):
        while self.running:
            try:
                text = self.voice_recognition.recognize_speech()
                if text:
                    intent = self.intent_handler.detect_intent(text)
                    if intent == "play_music":
                        Thread(target=self.handle_play_music, args=(text,)).start()
                    elif intent == "stop":
                        self.stop_audio_thread()  # Appel au stop avec contrôle
                        self.audio_feedback_signal.emit("Lecture arrêtée.")
                    else:
                        self.audio_feedback_signal.emit("Commande non comprise.")
            except Exception as e:
                self.audio_feedback_signal.emit(f"Erreur lors de la reconnaissance : {str(e)}")

    def handle_play_music(self, text):
        query = text.replace("mets", "").strip()
        self.audio_feedback_signal.emit(f"Recherche {query} sur YouTube.")
        try:
            results = self.youtube_player.search_youtube(query)
            if results:
                self.result_signal.emit(
                    "Résultats trouvés:\n" + "\n".join(
                        [f"{i + 1}: {title}" for i, (title, _) in enumerate(results)]
                    )
                )
                self.audio_feedback_signal.emit("Lecture de la première vidéo.")
                self.play_selected_video(0, results)  # Utilisation correcte
            else:
                self.audio_feedback_signal.emit("Aucun résultat trouvé.")
        except Exception as e:
            self.audio_feedback_signal.emit(f"Erreur lors de la recherche : {str(e)}")

    def play_selected_video(self, index, results):
        """
        Joue une vidéo en fonction de l'index sélectionné.
        """
        try:
            title, url = results[index]
            self.youtube_player.play_video(url)
            self.audio_feedback_signal.emit(f"Lecture de {title}.")
        except Exception as e:
            self.audio_feedback_signal.emit(f"Erreur lors de la lecture : {str(e)}")

    def stop_audio_thread(self):
        """Stoppe proprement le thread de lecture audio."""
        self.stop_event.set()  # Signal de stop envoyé
        self.youtube_player.stop()  # Arrêt propre si thread audio est actif

    def stop_thread(self):
        """Arrête le thread de reconnaissance vocale."""
        self.running = False
        self.stop_event.set()
