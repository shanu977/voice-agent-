from groq import Groq

from config import Config
from utils.logger import get_logger


logger = get_logger("STT")


class GroqSTT:

    def __init__(self):

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

        self.model = Config.STT_MODEL


    def transcribe(self, audio_file):
        """
        Convert speech to text

        Args:
            audio_file:
                Path of WAV file

        Returns:
            Text
        """

        try:

            logger.info(
                f"Transcribing audio: {audio_file}"
            )


            with open(
                audio_file,
                "rb"
            ) as file:


                result = self.client.audio.transcriptions.create(
                    file=file,
                    model=self.model,
                    response_format="text"
                )


            logger.info(
                "Transcription completed"
            )


            return result


        except Exception as e:

            logger.error(
                f"STT failed: {e}"
            )

            return None