import pyttsx3

class SpeechSynthesis:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
