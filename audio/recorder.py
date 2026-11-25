import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import time
from datetime import datetime

from config import Config
from utils.logger import get_logger


logger = get_logger("RECORDER")


class AudioRecorder:


    def __init__(self):

        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS



    # =====================================
    # Fixed duration recording
    # =====================================

    def record(self, duration=5):

        try:

            logger.info(
                "Recording started..."
            )


            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32"
            )


            sd.wait()


            return self.save_audio(audio)



        except Exception as e:

            logger.error(
                f"Recording failed: {e}"
            )

            return None





    # =====================================
    # Voice Activity Detection Recording
    # =====================================

    def record_until_speech(self):

        logger.info(
            "Listening..."
        )


        frames = []

        speech_started = False

        silence_counter = 0


        threshold = 0.0015


        max_time = 20


        start = time.time()



        try:


            while True:


                # timeout

                if time.time() - start > max_time:


                    logger.info(
                        "Listening timeout"
                    )

                    break



                chunk = sd.rec(

                    int(0.5 * self.sample_rate),

                    samplerate=self.sample_rate,

                    channels=self.channels,

                    dtype="float32"

                )


                sd.wait()



                volume = np.sqrt(
                    np.mean(
                        chunk ** 2
                    )
                )


                logger.info(
                    f"Volume: {volume:.5f}"
                )



                frames.append(chunk)



                # -------------------------
                # Detect voice
                # -------------------------

                if volume > threshold:


                    if not speech_started:


                        logger.info(
                            "Speech started"
                        )


                        speech_started = True



                    silence_counter = 0



                else:


                    if speech_started:


                        silence_counter += 1




                # -------------------------
                # Stop after silence
                # -------------------------

                if speech_started and silence_counter >= 3:


                    logger.info(
                        "Speech ended"
                    )

                    break



            if not speech_started:


                logger.info(
                    "No speech detected"
                )

                return None




            audio = np.concatenate(
                frames,
                axis=0
            )


            return self.save_audio(
                audio
            )



        except KeyboardInterrupt:


            logger.info(
                "Recording stopped"
            )

            return None




        except Exception as e:


            logger.error(
                f"VAD recording failed: {e}"
            )

            return None





    # =====================================
    # Save audio file
    # =====================================

    def save_audio(self, audio):


        os.makedirs(
            "recordings",
            exist_ok=True
        )



        filename = (

            "recordings/"

            f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

        )



        sf.write(

            filename,

            audio,

            self.sample_rate

        )



        logger.info(
            f"Audio saved: {filename}"
        )


        return filename