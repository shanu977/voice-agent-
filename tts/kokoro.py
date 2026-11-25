import os
from datetime import datetime

from kokoro import KPipeline
import soundfile as sf

from config import Config
from utils.logger import get_logger


logger = get_logger("TTS")


class KokoroTTS:

    def __init__(self):

        logger.info("Loading Kokoro model...")

        self.pipeline = KPipeline(
            lang_code=Config.TTS_LANGUAGE
        )


        logger.info(
            "Kokoro loaded"
        )


    def generate(self, text):

        """
        Convert text to speech

        Args:
            text:
                AI response text

        Returns:
            audio file path
        """


        try:

            logger.info(
                "Generating speech..."
            )


            os.makedirs(
                "tts/output",
                exist_ok=True
            )


            filename = (
                "tts/output/"
                f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            )


            generator = self.pipeline(
                text,
                voice=Config.TTS_VOICE
            )


            for _, _, audio in generator:

                sf.write(
                    filename,
                    audio,
                    24000
                )


                break


            logger.info(
                f"Speech saved: {filename}"
            )


            return filename


        except Exception as e:

            logger.error(
                f"TTS failed: {e}"
            )

            return None