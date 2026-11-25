print("APP FILE LOADED")

from dotenv import load_dotenv
load_dotenv()

from audio.recorder import AudioRecorder
from audio.player import AudioPlayer
from audio.device_selector import list_output_devices

from stt.groq import GroqSTT

from brain.service import BrainService

from tts.kokoro import KokoroTTS

from utils.logger import get_logger


import time


logger = get_logger("APP")


def get_device_index(device_type):
    devices = list_output_devices()

    if device_type == "speakers":
        for d in devices:
            name_lower = d["name"].lower()
            if any(kw in name_lower for kw in ["speaker", "realtek", "sound mapper", "primary sound driver"]):
                if "headphone" not in name_lower and "headset" not in name_lower:
                    return d["index"]
        return sd.default.device[1]

    elif device_type == "headphones":
        # First priority: WH-CH520 (user's known working headphones)
        for d in devices:
            name_lower = d["name"].lower()
            if "wh-ch520" in name_lower and "headphones" in name_lower and d["channels"] == 2:
                return d["index"]

        # Second priority: Other Bluetooth headphones (2 channel, not hands-free)
        for d in devices:
            name_lower = d["name"].lower()
            if any(kw in name_lower for kw in ["headphone", "headset", "earphone", "earbud", "wh-", "buds", "airpods"]):
                if d["channels"] == 2 and "hands-free" not in name_lower and "handsfree" not in name_lower:
                    return d["index"]

        # Fallback: any headphone-like device
        for d in devices:
            name_lower = d["name"].lower()
            if any(kw in name_lower for kw in ["headphone", "headset", "earphone", "earbud", "wh-", "buds", "airpods"]):
                return d["index"]

        return sd.default.device[1]

    return sd.default.device[1]


import sounddevice as sd


class VoiceAgent:


    def __init__(self, output_device_index=None):

        logger.info(
            "Starting Voice Agent..."
        )


        self.recorder = AudioRecorder()

        self.player = AudioPlayer(output_device_index=output_device_index)


        self.stt = GroqSTT()


        self.brain = BrainService()


        self.tts = KokoroTTS()


        logger.info(
            "Voice Agent Ready"
        )


    def run_once(self):

        try:

            print("\nListening...")

            audio_file = self.recorder.record_until_speech()

            if not audio_file:

                logger.info(
                    "No speech detected"
                )

                return False


            logger.info(
                "Converting speech..."
            )

            user_text = self.stt.transcribe(
                audio_file
            )

            if not user_text:

                logger.info(
                    "Empty transcription"
                )

                return False


            user_text = user_text.strip()


            ignored_words = [
                "",
                ".",
                "...",
                "Thank you.",
                "you"
            ]


            if user_text in ignored_words:

                logger.info(
                    "Ignored invalid speech"
                )

                return False


            print("\nYou:")
            print(user_text)


            logger.info(
                "Sending request to brain..."
            )

            response = self.brain.process(
                user_text
            )

            if not response:

                logger.warning(
                    "No AI response"
                )

                return False


            print("\nAI:")
            print(response)


            logger.info(
                "Generating voice..."
            )

            voice_file = self.tts.generate(
                response
            )

            if not voice_file:

                logger.warning(
                    "TTS failed"
                )

                return False


            self.player.play(
                voice_file
            )

            return True


        except Exception as e:

            logger.error(
                f"Agent error: {e}"
            )

            return False



if __name__ == "__main__":

    print("Select audio output device:")
    print("  1. Built-in speakers (default)")
    print("  2. Headphones / Headset / Earphones")
    print("  3. Use system default")

    while True:
        choice = input("Enter choice [1/2/3]: ").strip()
        if choice in ("1", "2", "3"):
            device_type = {"1": "speakers", "2": "headphones", "3": "default"}[choice]
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    if device_type == "default":
        output_device_index = None
    else:
        output_device_index = get_device_index(device_type)

    print(f"\nStarting voice agent...")

    agent = VoiceAgent(output_device_index=output_device_index)

    try:
        while True:
            print(
                "\n=============================="
            )
            print(
                "        AI Voice Agent"
            )
            print(
                "=============================="
            )
            print(
                "Speak now..."
            )
            print(
                "Press CTRL+C to stop"
            )
            print(
                "==============================\n"
            )

            success = agent.run_once()

            if not success:
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info(
            "Voice Agent stopped"
        )
        print(
            "\nVoice Agent closed."
        )