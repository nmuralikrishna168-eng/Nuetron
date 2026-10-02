import pyttsx3
import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal
from config import SPEECH_RATE, PAUSE_THRESHOLD, LISTEN_TIMEOUT


class SpeechEngine:
    """Text-to-Speech and voice processing engine."""

    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()
        self.engine.setProperty("rate", SPEECH_RATE)

    def _configure_voice(self):
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if "en" in voice.id.lower() or "zira" in voice.name.lower() or "david" in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                return
        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")


class VoiceListenerThread(QThread):
    command_received = pyqtSignal(str)
    status_updated = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = PAUSE_THRESHOLD

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            self.status_updated.emit("Listening for 'Neutron'...")

            while True:
                try:
                    audio = recognizer.listen(source, phrase_time_limit=LISTEN_TIMEOUT)
                    text = recognizer.recognize_google(audio).lower()

                    if "neutron" in text:
                        self.status_updated.emit("Wake-word detected!")
                        self.command_received.emit(text)
                    else:
                        self.status_updated.emit("Listening for 'Neutron'...")
                except sr.UnknownValueError:
                    self.status_updated.emit("Listening for 'Neutron'...")
                except sr.RequestError as e:
                    self.status_updated.emit(f"Audio Service Error: {e}")
                except Exception as e:
                    self.status_updated.emit(f"Audio Error: {e}")
