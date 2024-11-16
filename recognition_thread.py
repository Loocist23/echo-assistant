from PyQt5.QtCore import QThread, pyqtSignal
from voice_recognition import VoiceRecognition
from streaming_audio_player import StreamingAudioPlayer  # Nom du fichier mis à jour
from intent_handler import IntentHandler
from threading import Thread, Event
import pyttsx3
import time
import queue

class RecognitionThread(QThread):
    result_signal = pyqtSignal(str)
    audio_feedback_signal = pyqtSignal(str)

    def __init__(self, output_device):
        super().__init__()
        self.voice_recognition = VoiceRecognition()
        self.audio_player = StreamingAudioPlayer()
        self.intent_handler = IntentHandler()
        self.output_device = output_device
        self.running = True
        self.stop_event = Event()
        self.tts_queue = queue.Queue()
        self.tts_engine = pyttsx3.init()
        self.tts_thread = Thread(target=self.run_tts, daemon=True)
        self.tts_thread.start()

    def run(self):
        while self.running:
            try:
                self.speak("En attente de l'activation...")
                if self.listen_for_wake_word():
                    self.speak("Je vous écoute.")
                    self.listen_for_command()
            except Exception as e:
                self.speak(f"Erreur : {str(e)}")
                print(f"Erreur : {str(e)}")
                time.sleep(1)

    def listen_for_wake_word(self):
        """Écoute continue pour détecter le mot-clé d'activation."""
        while not self.stop_event.is_set():
            text = self.voice_recognition.recognize_speech()
            if text and ("ok écho" in text.lower() or "écho" in text.lower()):
                return True
            time.sleep(0.5)

    def listen_for_command(self):
        """Écoute la commande utilisateur après le mot-clé."""
        text = self.voice_recognition.recognize_speech()
        if text:
            intent = self.intent_handler.detect_intent(text)
            match intent:
                case "play_music":
                    Thread(target=self.handle_play_music, args=(text,)).start()
                case "stop":
                    self.stop_audio_thread()
                    self.speak("Lecture arrêtée.")
                case "set_volume":
                    percentage = self.intent_handler.extract_volume_percentage(text)
                    if percentage is not None:
                        self.audio_player.set_volume_by_percentage(percentage)
                        self.speak(f"Volume réglé à {percentage}%.")
                    elif "monte" in text or "augmente" in text:
                        self.audio_player.increase_volume()
                        self.speak("Volume augmenté.")
                    elif "baisse" in text or "diminue" in text:
                        self.audio_player.decrease_volume()
                        self.speak("Volume diminué.")
                    else:
                        self.speak("Commande de volume non comprise.")
                case _:
                    self.speak("Commande non comprise.")

    def handle_play_music(self, text):
        query = text.replace("mets", "").strip()
        self.speak(f"Recherche {query} sur YouTube.")
        try:
            results = self.audio_player.search_youtube(query)
            if results:
                self.result_signal.emit(
                    "Résultats trouvés:\n" + "\n".join(
                        [f"{i + 1}: {title}" for i, (title, _) in enumerate(results)]
                    )
                )
                self.speak("Lecture de la première vidéo.")
                self.play_selected_video(0, results)
            else:
                self.speak("Aucun résultat trouvé.")
        except Exception as e:
            self.speak(f"Erreur lors de la recherche : {str(e)}")

    def play_selected_video(self, index, results):
        try:
            title, url = results[index]
            self.audio_player.play_video(url)
            self.speak(f"Lecture de {title}.")
        except Exception as e:
            self.speak(f"Erreur lors de la lecture : {str(e)}")

    def stop_audio_thread(self):
        self.stop_event.set()
        self.audio_player.stop()
        self.reset_after_stop()

    def reset_after_stop(self):
        """Réinitialise l'événement et continue à écouter après un arrêt."""
        self.stop_event.clear()

    def stop_thread(self):
        """Arrête tout le thread de reconnaissance."""
        self.running = False
        self.stop_event.set()

    def speak(self, text):
        """Utilise TTS pour parler à l'utilisateur."""
        self.tts_queue.put(text)

    def run_tts(self):
        """Exécute le TTS dans un thread dédié."""
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
