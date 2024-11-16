import speech_recognition as sr

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def list_microphones(self):
        print("Microphones disponibles :")
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{i}: {name}")

    def recognize_speech(self):
        try:
            with self.microphone as source:
                print("Parlez maintenant...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit : {text}")
                return text
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit.")
            return None
        except sr.RequestError as e:
            print(f"Erreur du service Google Speech Recognition : {e}")
            return None
