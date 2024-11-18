# Echo - Assistant Vocal 🎤

Echo est un assistant vocal doté d'une interface graphique, capable d'effectuer des recherches sur Internet, de lire de la musique via YouTube, et bien plus encore.

## Fonctionnalités Actuelles 🚀

Les fonctionnalités de l'assistant sont basées sur des intentions détectées dans les commandes vocales de l'utilisateur. Voici ce que vous pouvez faire :

- **Lecture de Musique** : Commandez avec des phrases comme "mets", "joue", "écouter", "musique", ou "lancer".
- **Arrêt ou Pause** : Dites "arrête", "stop", "pause", ou "termine".
- **Contrôle du Volume** : Ajustez le volume avec des commandes comme "volume à", "monte le son", "baisse le son", ou "plus fort".
- **Calculs Vocaux** : Réalisez des opérations mathématiques simples en disant "calcule", "quel est le résultat", ou "fais l'addition".
- **Lecture des Nouvelles et Météo** : Informations actualisées sur les actualités et la météo.
- **Gestion des Tâches et Rappels** : Organisation et suivi des tâches quotidiennes.

## Fonctionnalités à Venir 🔮

- **Connexion à Spotify et Deezer** : Pour une expérience musicale encore plus personnalisée.
- **Recherche Internet Avancée** : Poser des questions complexes et obtenir des réponses détaillées.
- **Contrôle Domotique** : Intégration avec des appareils intelligents pour contrôler la maison (lumières, thermostat, etc.).
- **Mode Multilingue** : Support pour plusieurs langues afin de s'adapter à un public international.
- **Historique des Commandes** : Consultez les dernières commandes vocales pour faciliter l'utilisation.
- **Mode Hors Ligne** : Utilisation des fonctionnalités de base sans connexion Internet.

## Prérequis 🛠️

- **Python** : Version 3.8 ou supérieure.
- **Bibliothèques Python** :
  - PyQt5
  - pytube
  - pyttsx3
  - speech_recognition
  - pyaudio
  - yt_dlp
  - numpy
  - pydub
  - requests
  - python-dotenv
- **Fichier** .env
    ```
    NEWS_API_KEY=YOUR_NEWS_API_KEY
    WEATHER_API_KEY=YOUR_WEATHER_API_KEY
    ```

## Installation 💻

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Loocist23/echo-assistant.git
   cd echo-assistant
   ```
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Lancer l'application** :
   ```bash
   python main.py
   ```

## Utilisation 🎯

- **Démarrer la reconnaissance vocale** : Cliquez sur "Lancer la reconnaissance vocale" pour donner des commandes vocales.
- **Navigation** : Utilisez les boutons pour naviguer entre les différentes fonctionnalités.

## Contribuer 🤝

Les contributions sont les bienvenues ! Pour signaler un problème ou proposer une nouvelle fonctionnalité, ouvrez une issue sur le dépôt GitHub.

## Licence 📄

Ce projet est sous licence MIT. Voir le fichier [LICENCE](LICENCE) pour plus de détails.

*Date : 17 novembre 2024*
*Autheur: Loocist23*
