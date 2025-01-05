## echoes

A powerful Python tool for automatically transcribing and summarizing audio content from meetings, podcasts, and lectures. The system uses state-of-the-art speech recognition and natural language processing to generate summaries, extract action items, and integrate with task management and calendar systems.

### Features:
- Audio Processing
    - Support for multiple audio formats (WAV, MP3, M4A, OGG)
    - Automatic audio normalization
    - High-quality speech-to-text transcription
    - Multi-language support

- Content Analysis
    - Intelligent content summarization using BART
    - Key points extraction
    - Action item identification
    - Priority assignment

- Integrations
    - Task management system integration
    - Calendar integration for follow-up meetings
    - Email extraction for meeting participants

### Installation:
1. Clone the repository:
```bash
git clone https://github.com/themillenniumfalcon/echoes
cd echoes
```

2. Run the installation script:
```bash
python scripts/install_dependencies.py
```

This will:
- Create a virtual environment
- Install all required dependencies
- Install development dependencies
- Download required language models

### Configuration:
Create a .env file in the project root:
```bash
# API Keys
OPENAI_API_KEY=your_openai_key
GOOGLE_CLOUD_API_KEY=your_google_key
TASK_MANAGER_API_KEY=your_task_manager_key
CALENDAR_API_KEY=your_calendar_key

# Service Settings
TASK_MANAGER_URL=https://api.taskmanager.com
CALENDAR_SERVICE=google

# Audio Processing
DEFAULT_LANGUAGE=en-US
MAX_AUDIO_LENGTH_MINUTES=120

# Summarization
MAX_SUMMARY_LENGTH=130
MIN_SUMMARY_LENGTH=30
SUMMARIZER_MODEL=facebook/bart-large-cnn

# Logging
LOG_LEVEL=INFO
LOG_FILE=audio_summarizer.log
```

### Usage:
#### Command Line Interface:
Process an audio file and generate a summary:
```bash
python -m src.cli input_audio.mp3 --output summary.json
```

Create tasks from action items:
```bash
python -m src.cli input_audio.mp3 --create-tasks
```

Schedule a follow-up meeting:
```bash
python -m src.cli input_audio.mp3 --schedule-followup
```

#### Python API:
```bash
from audio_summarizer import AudioSummarizer

# Initialize the summarizer
summarizer = AudioSummarizer()

# Process an audio file
results = summarizer.process_audio_file(
    "meeting_recording.mp3",
    create_tasks=True,
    schedule_followup=True
)

# Access results
print("Summary:", results["summary"])
print("Action Items:", results["action_items"])
print("Created Tasks:", results["tasks"])
```

#### Async API:
```bash
import asyncio
from audio_summarizer import create_async_summarizer

async def process_audio():
    async with await create_async_summarizer() as summarizer:
        results = await summarizer.process_audio_file_async(
            "meeting_recording.mp3"
        )
        return results

# Run async processing
results = asyncio.run(process_audio())
```

### Development:
#### Running Tests:
Run the test suite with coverage report:
```bash
python scripts/run_tests.py
```

#### Project Structure:
```bash
echoes/
├── src/
│   ├── audio/         # Audio processing components
│   ├── config/        # Configuration management
│   ├── integrations/  # External service integrations
│   ├── nlp/           # NLP and summarization
│   └── utils/         # Utility functions
├── tests/             # Test suites
└── scripts/           # Utility scripts
```