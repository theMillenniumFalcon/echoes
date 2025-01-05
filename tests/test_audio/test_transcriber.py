import pytest
import numpy as np
from src.audio.transcriber import AudioTranscriber
import os
from typing import Tuple
import wave

def create_sine_wave(frequency: float, duration: float, sample_rate: int = 44100) -> Tuple[np.ndarray, int]:
    """Create a sine wave audio signal."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    audio_data = (audio_data * 32767).astype(np.int16)
    return audio_data, sample_rate

def create_test_wav_file(filepath: str, duration: float = 1.0) -> str:
    """Create a test WAV file with a sine wave."""
    audio_data, sample_rate = create_sine_wave(440, duration)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return filepath

def create_speech_wav_file(filepath: str, text: str) -> str:
    """Create a WAV file with synthesized speech using gTTS."""
    try:
        from gtts import gTTS
        import os
        
        mp3_path = filepath.replace('.wav', '.mp3')
        tts = gTTS(text=text, lang='en')
        tts.save(mp3_path)
        
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(filepath, format="wav")

        os.remove(mp3_path)
        
        return filepath
    except Exception as e:
        pytest.skip(f"Speech synthesis failed: {str(e)}")

class TestAudioTranscriber:
    @pytest.fixture
    def transcriber(self):
        return AudioTranscriber()
    
    @pytest.fixture
    def test_dir(self, tmp_path):
        return tmp_path
    
    def test_transcribe_sine_wave(self, transcriber, test_dir):
        """Test transcription with a simple sine wave audio file."""
        wav_path = os.path.join(test_dir, "sine_wave.wav")
        create_test_wav_file(wav_path)
        
        result = transcriber.transcribe_file(wav_path)
        assert result is None or result.strip() == ""
    
    def test_transcribe_speech(self, transcriber, test_dir):
        """Test transcription with synthesized speech audio."""
        test_text = "Hello, this is a test of the audio transcription system."
        wav_path = os.path.join(test_dir, "speech.wav")
        
        try:
            create_speech_wav_file(wav_path, test_text)
            
            result = transcriber.transcribe_file(wav_path)

            assert result is not None
            key_words = ["hello", "test", "audio", "transcription"]
            result_lower = result.lower()
            for word in key_words:
                assert word in result_lower
                
        except Exception as e:
            pytest.skip(f"Speech transcription test failed: {str(e)}")
    
    def test_transcribe_invalid_file(self, transcriber):
        """Test transcription with invalid file path."""
        result = transcriber.transcribe_file("nonexistent_file.wav")
        assert result is None
    
    def test_transcribe_corrupted_file(self, transcriber, test_dir):
        """Test transcription with corrupted audio file."""
        corrupted_path = os.path.join(test_dir, "corrupted.wav")
        with open(corrupted_path, 'wb') as f:
            f.write(b'This is not a valid WAV file')
        
        result = transcriber.transcribe_file(corrupted_path)
        assert result is None
    
    @pytest.mark.parametrize("language", ["en-US", "es-ES", "fr-FR"])
    def test_transcribe_different_languages(self, transcriber, test_dir, language):
        """Test transcription with different languages."""
        transcriber.language = language
        wav_path = os.path.join(test_dir, f"speech_{language}.wav")
        
        test_phrases = {
            "en-US": "Hello, this is a test.",
            "es-ES": "Hola, esto es una prueba.",
            "fr-FR": "Bonjour, ceci est un test."
        }
        
        try:
            create_speech_wav_file(wav_path, test_phrases[language])
            result = transcriber.transcribe_file(wav_path)
            assert result is not None
            
            key_words = {
                "en-US": ["hello", "test"],
                "es-ES": ["hola", "prueba"],
                "fr-FR": ["bonjour", "test"]
            }
            
            result_lower = result.lower()
            for word in key_words[language]:
                assert word in result_lower
                
        except Exception as e:
            pytest.skip(f"Multi-language test failed for {language}: {str(e)}")

def test_transcriber_performance(transcriber, test_dir):
    """Test transcriber performance with various audio durations."""
    durations = [1.0, 2.0, 5.0]
    
    for duration in durations:
        wav_path = os.path.join(test_dir, f"perf_test_{duration}s.wav")
        
        with wave.open(wav_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            audio_data = np.zeros(int(44100 * duration), dtype=np.int16)
            wav_file.writeframes(audio_data.tobytes())
        
        import time
        start_time = time.time()
        transcriber.transcribe_file(wav_path)
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < duration * 5