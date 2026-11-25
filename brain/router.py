from brain.intent import IntentClassifier
from brain.decision import DecisionEngine
from brain.planner import Planner


from utils.logger import get_logger



logger = get_logger("BRAIN_ROUTER")



class BrainRouter:



    def __init__(self):


        self.intent = IntentClassifier()

        self.decision = DecisionEngine()

        self.planner = Planner()




    def process(
        self,
        user_text
    ):


        logger.info(
            "Brain processing..."
        )



        intent = self.intent.classify(
            user_text
        )



        decision = self.decision.decide(
            intent
        )



        plan = self.planner.create_plan(

            intent,

            decision

        )



        return {


            "intent": intent,


            "decision": decision,


            "plan": plan

        }