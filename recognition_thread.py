import re
import os
from dotenv import load_dotenv  # Charger les variables d'environnement
from PyQt5.QtCore import QThread, pyqtSignal
from news_and_weather import NewsAndWeather
from ollama_handler import OllamaHandler
from task_manager import TaskManager
from voice_calculator import VoiceCalculator
from voice_recognition import VoiceRecognition
from streaming_audio_player import StreamingAudioPlayer
from intent_handler import IntentHandler
from threading import Thread, Event
from dateutil import parser
import pyttsx3
import time
import queue
import json

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
        self.ollama_handler = OllamaHandler()  # Initialisation du gestionnaire Ollama

        # Charger les clés API depuis les variables d'environnement
        news_api_key = os.getenv("NEWS_API_KEY")
        weather_api_key = os.getenv("WEATHER_API_KEY")

        self.news_and_weather = NewsAndWeather(news_api_key=news_api_key, weather_api_key=weather_api_key)
        self.tts_thread = Thread(target=self.run_tts, daemon=True)
        self.tts_thread.start()

        Thread(target=self.check_task_reminders, daemon=True).start()  # Ajout ici

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
            # Envoyer la commande à Ollama pour déterminer l'intention
            ollama_handler = OllamaHandler()
            response = ollama_handler.send_command(text)

            # Parse la réponse d'Ollama
            if "play music" in response:
                content = self.extract_json_content(response)
                Thread(target=self.handle_play_music, args=(content["content"],)).start()
            elif "stop" in response:
                self.stop_audio_thread()
                self.speak("Lecture arrêtée.")
            elif "calculate" in response:
                expression = self.extract_json_content(response).get("expression")
                result = self.voice_calculator.parse_and_calculate(expression)
                self.speak(result)
            elif "set volume" in response:
                volume = self.extract_json_content(response).get("volume")
                if volume is not None:
                    self.audio_player.set_volume_by_percentage(volume)
                    self.speak(f"Volume réglé à {volume}%.")
            elif "weather" in response:
                city = self.extract_json_content(response).get("city", "Paris")
                weather_info = self.news_and_weather.get_weather(city)
                self.speak(weather_info)
            elif "add task" in response:
                task_info = self.extract_json_content(response)
                task_name = task_info.get("task")
                reminder_time = task_info.get("reminder_time")
                response = self.task_manager.add_task(task_name, reminder_time)
                self.speak(response)
            elif "news" in response:
                self.speak("Voici les dernières nouvelles.")
                news = self.news_and_weather.get_news()
                for article in news:
                    self.speak(article)
            else:
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

    def extract_reminder_time(self, text):
        """
        Extrait la date et l'heure de rappel depuis le texte.
        """
        try:
            # Recherche améliorée des termes liés au rappel
            match = re.search(r"(à|le|dans)\s(.+)", text)
            if match:
                reminder_text = match.group(2)
                # Utilise `fuzzy=True` pour interpréter même des textes imparfaits
                reminder_time = parser.parse(reminder_text, fuzzy=True, dayfirst=True)
                return reminder_time
        except Exception as e:
            print(f"Erreur lors de l'extraction de la date : {e}")
        return None

    def check_task_reminders(self):
        """
        Vérifie périodiquement les rappels.
        """
        while self.running:
            reminders = self.task_manager.check_reminders()
            for task in reminders:
                self.speak(f"Rappel : {task}")
            time.sleep(60)  # Vérifie toutes les minutes

    def extract_json_content(self, response):
        """
        Extrait le contenu JSON de la réponse renvoyée par Ollama.
        """
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"Erreur lors de l'extraction JSON : {e}")
            return {}
