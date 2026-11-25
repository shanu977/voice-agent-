import sounddevice as sd
import soundfile as sf
import numpy as np

from utils.logger import get_logger


logger = get_logger("PLAYER")


class AudioPlayer:


    def __init__(self, output_device_index=None):
        self.output_device_index = output_device_index


    def play(self, file_path):

        try:

            logger.info(
                f"Playing audio: {file_path}"
            )


            audio, sample_rate = sf.read(
                file_path,
                dtype="float32"
            )


            if len(audio.shape) == 1:

                channels = 1

            else:

                channels = audio.shape[1]


            logger.info(
                f"Sample rate: {sample_rate}, Channels: {channels}"
            )


            # Amplify audio (Kokoro output is often quiet)
            rms = np.sqrt(np.mean(audio**2))
            if rms > 0:
                gain = min(0.8 / rms, 10.0)
                audio = audio * gain
                audio = np.clip(audio, -1.0, 1.0)
                logger.info(f"Applied gain: {gain:.2f}x")


            devices = sd.query_devices()


            output_device = self.output_device_index

            if output_device is None:
                # Fallback: prefer WH-CH520 headphones
                for index, device in enumerate(devices):
                    if device["max_output_channels"] > 0 and "WH-CH520" in device["name"] and "Headphones" in device["name"]:
                        output_device = index
                        break

                if output_device is None:
                    for index, device in enumerate(devices):
                        if device["max_output_channels"] > 0:
                            output_device = index
                            break


            if output_device is None:

                raise Exception(
                    "No output device found"
                )


            logger.info(
                f"Using output device: {output_device} - {devices[output_device]['name']}"
            )


            sd.play(
                audio,
                samplerate=sample_rate,
                device=output_device
            )


            sd.wait()


            logger.info(
                "Audio playback completed"
            )


        except Exception as e:

            logger.error(
                f"Playback failed: {e}"
            )