from utils.logger import get_logger


logger = get_logger("DECISION")



class DecisionEngine:



    def decide(self, intent):


        decisions = {


            "time":
                "use_tool",


            "calculation":
                "use_tool",


            "conversation":
                "llm",


            "general":
                "llm"

        }



        decision = decisions.get(
            intent,
            "llm"
        )



        logger.info(
            f"Decision: {decision}"
        )



        return decision