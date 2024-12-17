import requests


class OllamaHandler:
    """
    Gestionnaire pour interagir avec l'API Ollama.
    Envoie une commande texte à un modèle de langage (ex: Mistral 7B) et récupère l'intention.
    """

    def __init__(self, api_url="http://127.0.0.1:11434/api/generate", model="mistral"):
        """
        Initialise le gestionnaire Ollama.

        :param api_url: URL de l'API Ollama locale.
        :param model: Nom du modèle utilisé (par exemple, 'mistral').
        """
        self.api_url = api_url
        self.model = model

    def send_command(self, command):
        """
        Envoie une commande à Ollama et récupère la réponse formatée.

        :param command: Texte de la commande utilisateur.
        :return: Réponse d'Ollama contenant l'intention et les détails.
        """
        # Prompt pour Ollama basé sur le contexte d'Echo
        prompt = f"""
        Tu es un assistant vocal intégré nommé "Echo". Ton rôle est d'interpréter les commandes vocales des utilisateurs 
        et de déterminer l'action correspondante. Voici ce que tu peux faire :

        1. Lecture de musique :
           - Commandes possibles : "mets [artiste/titre]", "joue [titre]", "écouter [chanson/artiste]".
           - Action attendue : Retourne `play music` avec les détails du contenu (artiste/titre).

        2. Rappels et tâches :
           - Commandes possibles : "ajoute une tâche [description]", "rappelle-moi de [faire quelque chose] à [heure/date]".
           - Action attendue : Retourne `add task` avec la description et l'heure/la date si spécifiées.

        3. Calculs :
           - Commandes possibles : "calcule [expression mathématique]", "combien font [x et y]".
           - Action attendue : Retourne `calculate` avec l'expression mathématique.

        4. Régler le volume :
           - Commandes possibles : "baisse le son", "augmente le volume", "mets le volume à [niveau]".
           - Action attendue : Retourne `set volume` avec le niveau ou une indication d'augmentation/diminution.

        5. Météo et nouvelles :
           - Commandes possibles : "quel temps fait-il à [ville] ?", "donne-moi les nouvelles", "quelles sont les dernières nouvelles ?".
           - Action attendue : Retourne `weather` ou `news` avec les détails nécessaires (ville, catégorie, etc.).

        6. Autres commandes :
           - Si une commande ne correspond pas à une catégorie ci-dessus, retourne `unknown`.

        ### Exemple d'entrée :
        - Commande utilisateur : "Mets du Mozart."
        - Sortie attendue : `play music {{"content": "Mozart"}}`

        - Commande utilisateur : "Ajoute une tâche 'acheter du pain' demain à 9h."
        - Sortie attendue : `add task {{"task": "acheter du pain", "reminder_time": "demain à 9h"}}`

        - Commande utilisateur : "Quel temps fait-il à Paris ?"
        - Sortie attendue : `weather {{"city": "Paris"}}`

        ### Commande utilisateur :
        {command}

        Réponds uniquement avec l'intention et les détails nécessaires.
        """
        payload = {"model": self.model, "prompt": prompt, "stream": False}

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.RequestException as e:
            return f"Erreur de connexion avec Ollama : {e}"
        except Exception as e:
            return f"Erreur inattendue : {e}"
