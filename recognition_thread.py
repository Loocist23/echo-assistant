import re
import os
from dotenv import load_dotenv  # Charger les variables d'environnement
from PyQt5.QtCore import QThread, pyqtSignal
from news_and_weather import NewsAndWeather
from task_manager import TaskManager
from voice_calculator import VoiceCalculator
from voice_recognition import VoiceRecognition
from streaming_audio_player import StreamingAudioPlayer
from intent_handler import IntentHandler
from threading import Thread, Event
import pyttsx3
import time
import queue

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class RecognitionThread(QThread):
    result_signal = pyqtSignal(str)
    audio_feedback_signal = pyqtSignal(str)

    def __init__(self, output_device):
        super().__init__()
        self.voice_recognition = VoiceRecognition()
        self.audio_player = StreamingAudioPlayer()
        self.voice_calculator = VoiceCalculator()
        self.intent_handler = IntentHandler()
        self.task_manager = TaskManager()  # Nouveau gestionnaire de tâches
        self.output_device = output_device
        self.running = True
        self.stop_event = Event()
        self.tts_queue = queue.Queue()
        self.tts_engine = pyttsx3.init()

        # Charger les clés API depuis les variables d'environnement
        news_api_key = os.getenv("NEWS_API_KEY")
        weather_api_key = os.getenv("WEATHER_API_KEY")

        self.news_and_weather = NewsAndWeather(news_api_key=news_api_key, weather_api_key=weather_api_key)
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
                case "calculate":
                    result = self.voice_calculator.parse_and_calculate(text)
                    self.speak(result)
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
                case "news":
                    self.speak("Voici les dernières nouvelles.")
                    news = self.news_and_weather.get_news()
                    for article in news:
                        self.speak(article)
                case "weather":
                    city = self.extract_city(text)
                    weather_info = self.news_and_weather.get_weather(city)
                    self.speak(weather_info)
                case "task":
                    if "ajoute" in text or "note" in text:
                        task_name = text.replace("ajoute une tâche", "").strip()
                        response = self.task_manager.add_task(task_name)
                        self.speak(response)
                    elif "liste" or "quels" in text:
                        tasks = self.task_manager.list_tasks()
                        self.speak(tasks)
                    elif "supprime" in text:
                        task_name = text.replace("supprime la tâche", "").strip()
                        response = self.task_manager.remove_task(task_name)
                        self.speak(response)
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

    def extract_city(self, text):
        """Extrait la ville mentionnée dans le texte."""
        # Liste des villes connues à partir d'une base simplifiée
        known_cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Bordeaux", "Lille", "Nantes", "Strasbourg",
                        "Montpellier"]

        # Cherche une ville connue dans le texte
        for city in known_cities:
            if city.lower() in text.lower():
                return city

        # Si aucune ville connue n'est trouvée, tenter d'extraire un mot après 'à', 'de', 'dans', etc.
        match = re.search(r"à\s+(\w+)|dans\s+(\w+)|de\s+(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1) or match.group(2) or match.group(3)

        # Retourne 'Paris' par défaut si aucune ville n'est extraite
        return "Paris"