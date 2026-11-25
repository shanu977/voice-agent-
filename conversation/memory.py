from utils.logger import get_logger


logger = get_logger("MEMORY")


class ConversationMemory:

    def __init__(self, max_history=20):

        self.max_history = max_history

        self.messages = []


    def add_user_message(self, text):

        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )


        self._limit()


    def add_ai_message(self, text):

        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )


        self._limit()



    def get_history(self):

        return self.messages



    def clear(self):

        self.messages = []

        logger.info(
            "Conversation cleared"
        )



    def _limit(self):

        if len(self.messages) > self.max_history:

            self.messages = self.messages[
                -self.max_history:
            ]