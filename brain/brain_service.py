from brain.router import BrainRouter

from conversation.manager import ConversationManager

from utils.logger import get_logger


logger = get_logger("BRAIN_SERVICE")



class BrainService:


    def __init__(self):

        self.brain_router = BrainRouter()

        self.conversation = ConversationManager()



    def process(self, user_text):


        logger.info(
            "Brain processing request"
        )


        # Brain decision

        brain_result = self.brain_router.process(
            user_text
        )


        logger.info(
            f"Brain result: {brain_result}"
        )



        # Add user memory

        self.conversation.memory.add_user_message(
            user_text
        )



        # Generate response

        response = self.conversation.chat(
            user_text
        )



        # Save AI memory

        self.conversation.memory.add_ai_message(
            response
        )



        return response