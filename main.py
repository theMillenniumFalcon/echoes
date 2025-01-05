from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
from pathlib import Path

from .src.audio.transcriber import AudioTranscriber
from .src.audio.audio_processor import AudioProcessor
from .src.nlp.summarizer import ContentSummarizer
from .src.nlp.action_item_extractor import ActionItemExtractor
from .src.integrations.task_manager import TaskManager
from .src.integrations.calendar_integration import CalendarIntegration
from .src.config.settings import Settings
from .src.utils.helpers import extract_email_addresses

class AudioSummarizer:
    """Main class that orchestrates the audio summarization process."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.setup_logging()
        
        self.audio_processor = AudioProcessor()
        self.transcriber = AudioTranscriber(language=self.settings.DEFAULT_LANGUAGE)
        self.summarizer = ContentSummarizer(model_name=self.settings.SUMMARIZER_MODEL)
        self.action_extractor = ActionItemExtractor()

        self.task_manager = None
        self.calendar_integration = None
        
        if self.settings.TASK_MANAGER_API_KEY:
            self.task_manager = TaskManager(
                self.settings.TASK_MANAGER_API_KEY,
                self.settings.TASK_MANAGER_URL
            )
            
        if self.settings.CALENDAR_API_KEY:
            self.calendar_integration = CalendarIntegration(
                self.settings.CALENDAR_API_KEY,
                self.settings.CALENDAR_SERVICE
            )
    
    def setup_logging(self):
        """Configure logging for the application."""
        logging.basicConfig(
            level=getattr(logging, self.settings.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=self.settings.LOG_FILE
        )
        self.logger = logging.getLogger(__name__)

    def process_audio_file(self, file_path: str, create_tasks: bool = True, schedule_followup: bool = False) -> Dict:
        """Process an audio file and generate summary, action items, and integrations."""
        try:
            audio_path = file_path
            if not file_path.lower().endswith('.wav'):
                audio_path = self.audio_processor.convert_to_wav(file_path)
                if not audio_path:
                    raise ValueError(f"Failed to convert audio file: {file_path}")
            
            normalized_path = self.audio_processor.normalize_audio(audio_path)
            if not normalized_path:
                raise ValueError(f"Failed to normalize audio file: {audio_path}")
            
            transcript = self.transcriber.transcribe_file(normalized_path)
            if not transcript:
                raise ValueError(f"Failed to transcribe audio file: {normalized_path}")
            
            summary = self.summarizer.summarize(
                transcript,
                max_length=self.settings.MAX_SUMMARY_LENGTH,
                min_length=self.settings.MIN_SUMMARY_LENGTH
            )
            
            key_points = self.summarizer.extract_key_points(transcript)
            
            action_items = self.action_extractor.extract_action_items(transcript)
            
            tasks = []
            if create_tasks and self.task_manager and action_items:
                tasks = self.task_manager.create_tasks_from_action_items(action_items)
            
            calendar_event = None
            if schedule_followup and self.calendar_integration:
                attendees = extract_email_addresses(transcript)
                
                tomorrow = datetime.now().replace(hour=10, minute=0) + timedelta(days=1)
                calendar_event = self.calendar_integration.create_followup_meeting(
                    summary="Follow-up: " + summary[:50] + "...",
                    start_time=tomorrow,
                    attendees=attendees
                )
            
            results = {
                "transcript": transcript,
                "summary": summary,
                "key_points": key_points,
                "action_items": action_items,
                "tasks": tasks,
                "calendar_event": calendar_event
            }
            
            if audio_path != file_path:
                Path(audio_path).unlink(missing_ok=True)
            if normalized_path:
                Path(normalized_path).unlink(missing_ok=True)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing audio file: {str(e)}")
            raise

def create_async_summarizer():
    """Factory function for creating an async version of the summarizer."""
    from functools import partial
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    class AsyncAudioSummarizer(AudioSummarizer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.executor = ThreadPoolExecutor()
        
        async def process_audio_file_async(self, *args, **kwargs):
            """Async version of process_audio_file."""
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor,
                partial(self.process_audio_file, *args, **kwargs)
            )
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self):
            self.executor.shutdown(wait=True)
    
    return AsyncAudioSummarizer()