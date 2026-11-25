import torch
import soundfile as sf

from utils.logger import get_logger


logger = get_logger("VAD")


class VoiceActivityDetector:


    def __init__(self):

        logger.info(
            "Loading VAD model..."
        )


        self.model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False
        )


        (
            self.get_speech_timestamps,
            _,
            _,
            _,
            _
        ) = utils


        logger.info(
            "VAD loaded"
        )



    def detect(self, audio_file):

        try:

            logger.info(
                f"Checking speech: {audio_file}"
            )


            # Load wav using soundfile
            audio, sample_rate = sf.read(
                audio_file,
                dtype="float32"
            )


            # Convert numpy to torch tensor
            audio = torch.tensor(audio)


            # Ensure mono audio
            if len(audio.shape) > 1:

                audio = audio.mean(
                    dim=1
                )


            # Silero expects 16000 Hz
            if sample_rate != 16000:

                raise Exception(
                    f"Expected 16000Hz but got {sample_rate}"
                )



            speech = self.get_speech_timestamps(
                audio,
                self.model,
                sampling_rate=16000
            )



            if speech:

                logger.info(
                    "Speech detected"
                )

                return True


            logger.info(
                "No speech detected"
            )

            return False



        except Exception as e:


            logger.error(
                f"VAD failed: {e}"
            )


            return False