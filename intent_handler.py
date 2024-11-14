class IntentHandler:
    def __init__(self):
        self.intents = {
            "play_music": ["mets", "joue", "écouter", "musique", "lancer"],
            "stop": ["arrête", "stop", "pause", "termine", "stoppe"],
        }

    def detect_intent(self, text):
        for intent, keywords in self.intents.items():
            if any(keyword in text.lower() for keyword in keywords):
                return intent
        return "unknown"
