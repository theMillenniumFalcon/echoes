import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the audio summarizer."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
    TASK_MANAGER_API_KEY = os.getenv("TASK_MANAGER_API_KEY")
    CALENDAR_API_KEY = os.getenv("CALENDAR_API_KEY")
    
    TASK_MANAGER_URL = os.getenv("TASK_MANAGER_URL", "https://api.taskmanager.com")
    CALENDAR_SERVICE = os.getenv("CALENDAR_SERVICE", "google")
    
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en-US")
    MAX_AUDIO_LENGTH_MINUTES = int(os.getenv("MAX_AUDIO_LENGTH_MINUTES", "120"))
    
    MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", "130"))
    MIN_SUMMARY_LENGTH = int(os.getenv("MIN_SUMMARY_LENGTH", "30"))
    SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "audio_summarizer.log")