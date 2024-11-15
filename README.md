
# Echo - Assistant Vocal

**Echo** est un assistant vocal avec interface graphique, capable d'effectuer des recherches internet, de lire de la musique via YouTube, et bien plus à venir !

## Fonctionnalités Actuelles

- **Interface Graphique** : Simple et intuitive avec PyQt5.
- **Recherche Internet** : Effectue des recherches directement sur Google.
- **Lecture de Musique** : Joue des vidéos musicales depuis YouTube.
- **Commande Vocale** : Activation avec le mot-clé "Ok Echo" pour écouter et exécuter des commandes.
- **Synthèse Vocale (TTS)** : Réponse vocale pour une expérience utilisateur immersive.

## Fonctionnalités à Venir

- **Connexion à Spotify et Deezer** : Pour une expérience musicale encore plus personnalisée.
- **Intégration d'un Large Language Model (LLM)** : Pour des interactions avancées.
- **Gestion des Tâches et Rappels** : Ne manquez jamais un événement.
- **Contrôle Domotique** : Gérez vos appareils connectés.
- **Lecture de Nouvelles et Mises à Jour Météo** : Restez informé en temps réel.

## Prérequis

- **Python 3.8+**
- **Bibliothèques nécessaires** :
  ```bash
  pip install pyqt5 yt-dlp simpleaudio pyttsx3
  ```

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre_nom_utilisateur/echo-assistant.git
   cd echo-assistant
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```bash
   python main.py
   ```

## Utilisation

- L'assistant s'active avec le mot-clé "Ok Echo".
- Donnez des commandes vocales telles que "Mets PNL" ou "Stop".
- Utilisez les boutons pour tester les fonctionnalités de base via l'interface graphique.

## Idées Futures

Voici une liste d'idées pour les fonctionnalités futures :

- [X] **Traduction vocale en temps réel**.
- [X] **Synthèse vocale pour lire des réponses et interactions**.
- [ ] **Calculatrice vocale pour résoudre des équations**.
- [ ] **Lecture de flux RSS ou nouvelles personnalisées**.
- [ ] **Commandes pour contrôle domotique**.
- [ ] **Personnalisation via API externe (Météo, Trafic, etc.)**.

## Contribuer

Les contributions sont les bienvenues ! Pour signaler un problème ou proposer une nouvelle fonctionnalité, ouvrez une [issue](https://github.com/votre_nom_utilisateur/echo-assistant/issues).

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
