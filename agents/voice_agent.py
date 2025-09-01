# agents/voice_agent.py

import speech_recognition as sr
from core.event_bus import EventBus

class VoiceAgent:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        """Listen from microphone and publish user query as event."""
        with self.microphone as source:
            print("Listening... Speak now.")
            audio = self.recognizer.listen(source)

        try:
            query = self.recognizer.recognize_google(audio)
            print(f"Recognized: {query}")
            self.bus.publish("user_query", query)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Speech Recognition API unavailable.")
