class IntentHandler:
    def __init__(self):
        self.intents = {
            "play_music": ["mets", "joue", "écouter", "musique", "lancer"],
            "stop": ["arrête", "stop", "pause", "termine", "stoppe"],
            "set_volume": ["volume à", "monte le son", "baisse le son", "diminue le volume", "augmente le volume",
                           "plus fort", "moins fort"],
            "calculate": ["calcule", "quel est le résultat", "fais l'addition", "fais la soustraction", "multiplie",
                          "divise", "calcul", "combien fait"],
            "news": ["nouvelles", "actualités", "info", "infos"],
            "weather": ["météo", "temps", "fait-il", "prévisions"],
            "task": ["ajoute une tâche", "rappel", "souviens-toi", "note", "tâche", "rappels"],
        }

    def detect_intent(self, text):
        for intent, keywords in self.intents.items():
            if any(keyword in text.lower() for keyword in keywords):
                return intent
        return "unknown"

    def extract_volume_percentage(self, text):
        """
        Extrait un pourcentage de volume de la commande textuelle.
        Exemple : "Volume à 50%" -> 50
        """
        import re
        match = re.search(r'\b(\d+)\s*%', text)
        if match:
            return int(match.group(1))
        return None
