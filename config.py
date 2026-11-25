import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


class Config:

    # ==========================
    # Groq
    # ==========================

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )


    # ==========================
    # AI Models
    # ==========================

    # Speech To Text
    STT_MODEL = "whisper-large-v3-turbo"


    # Language Model
    LLM_MODEL = "allam-2-7b"



    # ==========================
    # Audio Settings
    # ==========================

    SAMPLE_RATE = 16000

    CHANNELS = 1

    CHUNK_SIZE = 1024



    # ==========================
    # Recording
    # ==========================

    MAX_RECORD_SECONDS = 30



    # ==========================
    # Conversation Memory
    # ==========================

    MAX_HISTORY = 20



    # ==========================
    # Kokoro TTS
    # ==========================

    TTS_LANGUAGE = "a"

    TTS_VOICE = "af_heart"



    # ==========================
    # Server
    # ==========================

    HOST = "0.0.0.0"

    PORT = 8000