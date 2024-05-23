import pyaudio
import speech_recognition as sr
import threading
import logging

class ContinuousListening:
    def __init__(self, master_neural):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.master_neural = master_neural
        self.listening_thread = threading.Thread(target=self.listen)
        self.is_listening = False

    def start_listening(self):
        self.is_listening = True
        self.listening_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.listening_thread.join()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    user_input = self.recognizer.recognize_google(audio)
                    logging.info(f"Recognized audio input: {user_input}")
                    response = self.master_neural.handle_intent(user_input)
                    logging.info(f"Response: {response}")
                except sr.WaitTimeoutError:
                    logging.info("Listening timeout, no speech detected.")
                except sr.UnknownValueError:
                    logging.error("Google Speech Recognition could not understand audio.")
                except sr.RequestError as e:
                    logging.error(f"Could not request results from Google Speech Recognition service; {e}")
