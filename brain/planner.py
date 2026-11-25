from utils.logger import get_logger


logger = get_logger("PLANNER")



class Planner:



    def create_plan(
        self,
        intent,
        decision
    ):


        plan = []



        if decision == "use_tool":


            plan.append(
                "execute_tool"
            )



        else:


            plan.append(
                "generate_response"
            )



        logger.info(
            f"Plan created: {plan}"
        )



        return plan