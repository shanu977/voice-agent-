import re

from utils.logger import get_logger


logger = get_logger("UNDERSTANDING")



class Understanding:


    def analyze(self, text):

        text = text.lower()



        result = {

            "intent": "chat",

            "entities": {}

        }



        # ==========================
        # Greeting
        # ==========================

        if any(
            word in text
            for word in [
                "hello",
                "hi",
                "hey"
            ]
        ):

            result["intent"] = "greeting"



        # ==========================
        # Name
        # ==========================

        elif "my name is" in text:


            name = text.replace(
                "my name is",
                ""
            ).strip()


            result["intent"] = "remember_name"

            result["entities"]["name"] = name



        # ==========================
        # Time
        # ==========================

        elif "time" in text:


            result["intent"] = "get_time"



        logger.info(
            f"Intent: {result}"
        )


        return result