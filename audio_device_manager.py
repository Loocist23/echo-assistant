import pyaudio
import pyttsx3


class AudioDeviceManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.input_device_index = None
        self.output_device_index = None

    def list_input_devices(self):
        """
        Liste les périphériques d'entrée disponibles.
        """
        devices = []
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                devices.append((i, info['name']))
        return devices

    def list_output_devices(self):
        """
        Liste les périphériques de sortie disponibles.
        """
        devices = []
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxOutputChannels'] > 0:
                devices.append((i, info['name']))
        return devices

    def set_input_device(self, index):
        """
        Définit le périphérique d'entrée sélectionné.
        """
        self.input_device_index = index

    def set_output_device(self, index):
        """
        Définit le périphérique de sortie sélectionné.
        """
        self.output_device_index = index

    def test_output_device(self, text="Test audio réussi !"):
        try:
            devices = self.list_output_devices()
            if self.output_device_index is None or self.output_device_index >= len(devices):
                raise ValueError("Périphérique de sortie audio invalide.")

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

            print(f"Test audio sur : {devices[self.output_device_index][1]} réussi.")
        except Exception as e:
            print(f"Erreur lors du test de la sortie audio : {e}")

    def test_input_device(self):
        """
        Teste le périphérique d'entrée sélectionné.
        """
        try:
            if self.input_device_index is None:
                raise ValueError("Aucun périphérique d'entrée sélectionné.")
            print(f"Test du périphérique d'entrée : {self.input_device_index}")
        except Exception as e:
            print(f"Erreur lors du test du périphérique d'entrée : {e}")
