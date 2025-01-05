import speech_recognition as sr
from typing import Optional
import logging

class AudioTranscriber:
    def __init__(self, language: str = "en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.logger = logging.getLogger(__name__)

    def transcribe_file(self, audio_file_path: str) -> Optional[str]:
        """Transcribe an audio file to text."""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio, language=self.language)
        except Exception as e:
            self.logger.error(f"Transcription error: {str(e)}")
            return None