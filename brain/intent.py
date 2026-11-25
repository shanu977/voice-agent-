from utils.logger import get_logger


logger = get_logger("INTENT")


class IntentClassifier:


    def __init__(self):

        pass



    def classify(self, text):


        text = text.lower()



        # Tool intents

        if "time" in text:

            return "time"



        if any(
            word in text
            for word in [
                "calculate",
                "plus",
                "minus",
                "multiply",
                "divide"
            ]
        ):

            return "calculation"



        # Conversation

        if any(
            word in text
            for word in [
                "hello",
                "hi",
                "hey"
            ]
        ):

            return "conversation"



        return "general"