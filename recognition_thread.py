from PyQt5.QtCore import QThread, pyqtSignal
from voice_recognition import VoiceRecognition
from youtube_player import YouTubePlayer
from intent_handler import IntentHandler

class RecognitionThread(QThread):
    result_signal = pyqtSignal(str)
    audio_feedback_signal = pyqtSignal(str)

    def __init__(self, output_device):
        super().__init__()
        self.voice_recognition = VoiceRecognition()
        self.youtube_player = YouTubePlayer()
        self.intent_handler = IntentHandler()
        self.output_device = output_device
        self.current_results = []

    def run(self):
        try:
            text = self.voice_recognition.recognize_speech()
            if text:
                intent = self.intent_handler.detect_intent(text)
                if intent == "play_music":
                    self.handle_play_music(text)
                elif intent == "stop":
                    self.youtube_player.stop()
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
                self.current_results = results
                self.result_signal.emit(
                    "Résultats trouvés:\n" + "\n".join(
                        [f"{i + 1}: {title}" for i, (title, _) in enumerate(results)]
                    )
                )
                self.audio_feedback_signal.emit("Lecture de la première vidéo.")
                self.play_selected_video(0)
            else:
                self.audio_feedback_signal.emit("Aucun résultat trouvé.")
        except Exception as e:
            self.audio_feedback_signal.emit(f"Erreur lors de la recherche : {str(e)}")

    def play_selected_video(self, index):
        try:
            if 0 <= index < len(self.current_results):
                title, url = self.current_results[index]
                self.youtube_player.play_video(url)
                self.audio_feedback_signal.emit(f"Lecture de {title}.")
            else:
                self.audio_feedback_signal.emit("Index de sélection invalide.")
        except Exception as e:
            self.audio_feedback_signal.emit(f"Erreur lors de la lecture : {str(e)}")
