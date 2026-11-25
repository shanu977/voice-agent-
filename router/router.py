from tools.registry import get_tool

from utils.logger import get_logger


logger = get_logger("ROUTER")



class ToolRouter:


    def execute(
        self,
        tool_name,
        input_data=None
    ):


        logger.info(
            f"Executing tool: {tool_name}"
        )



        tool = get_tool(
            tool_name
        )



        if not tool:


            return (
                f"Tool {tool_name} not available"
            )



        try:


            if input_data:


                return tool(
                    input_data
                )


            return tool()



        except Exception as e:


            logger.error(
                f"Tool execution failed: {e}"
            )


            return None