# AI Voice Agent

A real-time voice assistant built with Python that listens, understands, thinks, and responds with natural speech.

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Audio     │────▶│    STT      │────▶│    Brain    │────▶│    TTS      │────▶│   Audio     │
│  Recorder   │     │  (Groq)     │     │  Service    │     │  (Kokoro)   │     │   Player    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Speech-to-Text** | Groq Whisper (via API) | Fast, accurate transcription |
| **LLM/Brain** | Groq (Llama/Mixtral) | Intent understanding, reasoning, tool use |
| **Text-to-Speech** | Kokoro TTS | Local, high-quality voice synthesis |
| **Audio I/O** | PyAudio / sounddevice | Real-time recording & playback |
| **VAD** | WebRTC VAD | Voice activity detection |
| **Logging** | Python logging | Structured debug/info/error logs |

---

## Project Structure

```
voice-agent/
├── app.py                 # Main entry point & orchestration loop
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # API keys (GROQ_API_KEY)
│
├── audio/                 # Audio input/output
│   ├── recorder.py        # Records until speech detected (VAD)
│   ├── player.py          # Plays generated audio
│   └── vad.py             # Voice Activity Detection wrapper
│
├── stt/                   # Speech-to-Text
│   └── groq.py            # Groq Whisper API client
│
├── brain/                 # Core intelligence
│   ├── service.py         # Main BrainService orchestration
│   ├── brain_service.py   # High-level brain logic
│   ├── router.py          # Routes to tools vs direct response
│   ├── planner.py         # Plans multi-step actions
│   ├── intent.py          # Classifies user intent
│   └── decision.py        # Makes execution decisions
│
├── conversation/          # Conversation management
│   ├── manager.py         # Conversation state & history
│   ├── memory.py          # Short-term memory
│   └── prompt.py          # System prompts
│
├── llm/                   # LLM providers
│   └── groq.py            # Groq API client
│
├── tts/                   # Text-to-Speech
│   └── kokoro.py          # Kokoro TTS wrapper
│
├── tools/                 # Tool ecosystem
│   ├── registry.py        # Tool registration & dispatch
│   ├── manager.py         # Tool execution manager
│   ├── schemas.py         # Tool definitions (JSON Schema)
│   ├── calculator.py      # Math operations
│   ├── time_tool.py       # Current time/date
│   ├── weather_tool.py    # Weather queries
│   └── system_tool.py     # System commands
│
├── understanding/         # Input analysis
│   └── analyzer.py        # Semantic analysis
│
├── router/                # Request routing
│   └── router.py          # Routes requests to handlers
│
├── memory/                # Persistent memory
│   └── manager.py         # Long-term memory storage
│
├── utils/                 # Utilities
│   ├── logger.py          # Structured logging
│   └── json_parser.py     # JSON parsing helpers
│
├── logs/                  # Runtime logs
│   └── voice_agent.log    # Application logs
│
├── recordings/            # Saved audio recordings
│
├── tts/output/            # Generated speech audio
│
└── tests/                 # Unit tests
    ├── test_brain.py
    ├── test_brain_service.py
    ├── test_memory.py
    ├── test_new_tools.py
    └── test_tools.py
```

---

## How It Works

### 1. Audio Recording (`audio/recorder.py`)
- Uses PyAudio + WebRTC VAD
- Records continuously until speech is detected
- Stops after silence threshold (configurable)
- Saves to temporary WAV file

### 2. Speech-to-Text (`stt/groq.py`)
- Sends audio to Groq Whisper API
- Returns transcribed text
- Handles API errors & retries

### 3. Brain Processing (`brain/service.py`)
```
User Text → Intent Analysis → Route (Tool vs Direct) → Execute → Response
```
- **Intent Classification**: Determines what user wants
- **Routing**: Decides if tools needed or direct LLM response
- **Tool Execution**: Runs registered tools (calculator, weather, etc.)
- **Response Generation**: Formats final answer

### 4. Text-to-Speech (`tts/kokoro.py`)
- Uses Kokoro TTS (local, no API key needed)
- Generates natural-sounding speech
- Saves to `tts/output/`

### 5. Audio Playback (`audio/player.py`)
- Plays generated WAV file
- Blocks until complete

---

## Configuration

### `config.py`
```python
# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
VAD_AGGRESSIVENESS = 3  # 0-3

# Silence detection
SILENCE_THRESHOLD = 1.5  # seconds
MIN_SPEECH_DURATION = 0.5

# TTS
TTS_VOICE = "af_heart"  # Kokoro voice
TTS_SPEED = 1.0

# Brain
MAX_HISTORY = 10
TEMPERATURE = 0.7
```

### `.env`
```bash
GROQ_API_KEY=your_groq_api_key_here
```

---

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `calculator` | Basic math operations | "What's 15 * 23?" |
| `time_tool` | Current date/time | "What time is it?" |
| `weather_tool` | Weather queries | "Weather in London" |
| `system_tool` | System commands | "List files in home" |

Tools are defined in `tools/schemas.py` using JSON Schema.

---

## Running the Agent

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure .env has GROQ_API_KEY
# (already configured in this project)

# 3. Run
python app.py
```

### Controls
- **Speak** naturally - agent detects voice automatically
- **Ctrl+C** - Stop the agent
- **Wait** for "Listening..." prompt before speaking

---

## Adding New Tools

1. Create tool in `tools/your_tool.py`:
```python
def your_function(param: str) -> str:
    return f"Result: {param}"

TOOL_SCHEMA = {
    "name": "your_tool",
    "description": "What it does",
    "parameters": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Input"}
        },
        "required": ["param"]
    }
}
```

2. Register in `tools/registry.py`:
```python
from tools.your_tool import your_function, TOOL_SCHEMA

registry.register("your_tool", your_function, TOOL_SCHEMA)
```

3. The brain will automatically discover and use it.

---

## Logging

Logs written to `logs/voice_agent.log` with levels:
- **INFO**: Normal operation (listening, processing, speaking)
- **WARNING**: Recoverable issues (empty transcription, TTS fail)
- **ERROR**: Failures (API errors, crashes)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No speech detected" | Check microphone permissions; speak louder/closer |
| "Empty transcription" | Reduce background noise; check VAD settings |
| "TTS failed" | Verify Kokoro installation; check `tts/output/` permissions |
| "Groq API error" | Verify API key in `.env`; check rate limits |
| Audio device errors | Install PyAudio: `pip install pyaudio` (may need system deps) |

---

## Dependencies

```
groq                    # Groq API client
pyaudio                 # Audio I/O (may need: pip install pyaudio)
webrtcvad              # Voice activity detection
numpy                  # Audio processing
kokoro                 # TTS engine
soundfile              # Audio file handling
python-dotenv          # Environment variables
```

Install all: `pip install -r requirements.txt`

---

## Development

### Run Tests
```bash
python -m pytest tests/ -v
```

### Code Style
- Python 3.10+
- Type hints where practical
- Structured logging via `utils.logger`
- Modular, single-responsibility modules

---

## License

MIT License - Feel free to use and modify.