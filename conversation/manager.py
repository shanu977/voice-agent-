from brain.service import BrainService

from utils.logger import get_logger



logger = get_logger("CONVERSATION")



class ConversationManager:


    def __init__(self):


        self.brain = BrainService()



    def chat(self, user_text):


        logger.info(
            "User message received"
        )


        response = self.brain.process(
            user_text
        )


        logger.info(
            "Conversation completed"
        )


        return response