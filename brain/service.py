from brain.router import BrainRouter

from conversation.memory import ConversationMemory
from llm.groq import GroqLLM

from utils.logger import get_logger


logger = get_logger("BRAIN_SERVICE")



class BrainService:


    def __init__(self):


        self.router = BrainRouter()


        self.memory = ConversationMemory(
            max_history=20
        )


        self.llm = GroqLLM()



    def process(self, user_text):


        try:


            logger.info(
                "Brain processing request"
            )



            # =========================
            # 1. Analyze request
            # =========================

            brain_result = self.router.process(
                user_text
            )



            logger.info(
                f"Brain result: {brain_result}"
            )



            # =========================
            # 2. Save user message
            # =========================

            self.memory.add_user_message(
                user_text
            )



            # =========================
            # 3. LLM Response
            # =========================

            response = self.llm.generate(

                user_text,

                self.memory.get_history()

            )



            # =========================
            # 4. Save AI response
            # =========================

            self.memory.add_ai_message(
                response
            )



            return response



        except Exception as e:


            logger.error(
                f"Brain failed: {e}"
            )


            return None