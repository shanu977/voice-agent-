from tools.time_tool import get_current_time
from tools.calculator import calculate

from utils.logger import get_logger


logger = get_logger("TOOL_REGISTRY")



# =====================================
# Tool Functions Registry
# =====================================

TOOLS = {


    "get_time": get_current_time,


    "calculate": calculate


}





# =====================================
# Tool Information
# Used by LLM to understand tools
# =====================================

TOOLS_INFO = {


    "get_time": {

        "name": "get_time",

        "description":
        "Get the current time"


    },


    "calculate": {

        "name": "calculate",

        "description":
        "Perform mathematical calculations"


    }


}





# =====================================
# Get Tool Function
# =====================================

def get_tool(tool_name):


    tool = TOOLS.get(
        tool_name
    )



    if not tool:


        logger.warning(

            f"Tool not found: {tool_name}"

        )


        return None



    return tool





# =====================================
# Execute Tool
# =====================================

def execute_tool(tool_name, input_data=None):


    tool = get_tool(
        tool_name
    )



    if not tool:


        return (
            f"Tool {tool_name} not available"
        )



    try:


        if input_data is not None:


            return tool(
                input_data
            )


        return tool()



    except Exception as e:


        logger.error(

            f"Tool execution failed: {e}"

        )


        return None





# =====================================
# Get Available Tool Names
# =====================================

def get_available_tools():


    return list(
        TOOLS.keys()
    )





# =====================================
# Get Tool Descriptions
# =====================================

def get_tool_descriptions():


    return list(
        TOOLS_INFO.values()
    )





# =====================================
# Tool Schema For LLM
# =====================================

def get_tools_schema():


    return [

        {

            "name": tool["name"],

            "description": tool["description"]

        }

        for tool in TOOLS_INFO.values()

    ]