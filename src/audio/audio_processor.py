import os
from pydub import AudioSegment
from typing import Optional
import logging

class AudioProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = {
            'mp3': 'mp3',
            'wav': 'wav',
            'm4a': 'mp4',
            'ogg': 'ogg'
        }

    def convert_to_wav(self, file_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """Convert audio file to WAV format for transcription."""
        try:
            file_ext = os.path.splitext(file_path)[1][1:].lower()
            if file_ext not in self.supported_formats:
                self.logger.error(f"Unsupported file format: {file_ext}")
                return None

            audio = AudioSegment.from_file(file_path, format=self.supported_formats[file_ext])
            
            if not output_path:
                output_path = os.path.splitext(file_path)[0] + '.wav'
            
            audio.export(output_path, format='wav')
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error converting audio: {str(e)}")
            return None

    def normalize_audio(self, file_path: str, target_db: float = -20.0) -> Optional[str]:
        """Normalize audio volume to a target dB level."""
        try:
            audio = AudioSegment.from_wav(file_path)
            change_in_db = target_db - audio.dBFS
            normalized_audio = audio.apply_gain(change_in_db)
            
            output_path = os.path.splitext(file_path)[0] + '_normalized.wav'
            normalized_audio.export(output_path, format='wav')
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error normalizing audio: {str(e)}")
            return None