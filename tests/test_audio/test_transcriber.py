import pytest
from src.audio.transcriber import AudioTranscriber
import os

def test_transcriber_initialization():
    transcriber = AudioTranscriber()
    assert transcriber.language == "en-US"
    
def test_transcribe_file_with_invalid_path():
    transcriber = AudioTranscriber()
    result = transcriber.transcribe_file("nonexistent_file.wav")
    assert result is None

def test_transcribe_file_with_valid_file(tmp_path):
    # This is a mock test - in real implementation, you'd need a real audio file
    transcriber = AudioTranscriber()
    # Create a mock audio file
    audio_file = tmp_path / "test_audio.wav"
    audio_file.write_bytes(b"mock audio content")
    
    # Mock the recognizer's record and recognize_google methods
    def mock_recognize_google(*args, **kwargs):
        return "This is a test transcription"
    
    transcriber.recognizer.recognize_google = mock_recognize_google
    
    result = transcriber.transcribe_file(str(audio_file))
    assert isinstance(result, str)
    assert "test transcription" in result.lower()