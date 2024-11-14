class IntentHandler:
    def __init__(self):
        self.intents = {
            "play_music": ["mets", "joue", "musique", "écouter", "lancer de la musique"],
            # Ajouter d'autres intentions si nécessaire
        }

    def detect_intent(self, text):
        if any(keyword in text.lower() for keyword in self.intents["play_music"]):
            return "play_music"
        return "unknown"
