from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QComboBox
from recognition_thread import RecognitionThread
from audio_device_manager import AudioDeviceManager
import sys

class EchoApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_manager = AudioDeviceManager()
        self.initUI()
        self.thread = None
        self.start_recognition()

    def initUI(self):
        self.setWindowTitle('Echo - Assistant Vocal')
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        self.input_device_combo = QComboBox(self)
        self.input_device_combo.addItems([name for _, name in self.audio_manager.list_input_devices()])
        layout.addWidget(self.input_device_combo)

        self.output_device_combo = QComboBox(self)
        self.output_device_combo.addItems([name for _, name in self.audio_manager.list_output_devices()])
        layout.addWidget(self.output_device_combo)

        self.test_button = QPushButton('Tester Sortie Audio', self)
        self.test_button.clicked.connect(self.test_audio_output)
        layout.addWidget(self.test_button)

        self.setLayout(layout)

    def start_recognition(self):
        try:
            output_device_index = self.output_device_combo.currentIndex()
            if output_device_index < 0:
                self.text_display.append("Aucun périphérique de sortie sélectionné.")
                return

            output_device_name = self.audio_manager.list_output_devices()[output_device_index][1]
            self.thread = RecognitionThread(output_device_name)
            self.thread.result_signal.connect(self.display_result)
            self.thread.audio_feedback_signal.connect(self.display_result)
            self.thread.start()
        except Exception as e:
            self.text_display.append(f"Erreur lors du démarrage de la reconnaissance : {e}")

    def test_audio_output(self):
        try:
            self.audio_manager.set_output_device(self.output_device_combo.currentIndex())
            self.audio_manager.test_output_device()
            self.text_display.append("Test de la sortie audio réussi.")
        except Exception as e:
            self.text_display.append(f"Erreur lors du test de la sortie audio : {e}")

    def display_result(self, text):
        self.text_display.append(text)
