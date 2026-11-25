from groq import Groq
import json


from config import Config
from utils.logger import get_logger
from conversation.prompt import SYSTEM_PROMPT

from router.router import ToolRouter
from tools.schemas import TOOLS_SCHEMA


logger = get_logger("LLM")



class GroqLLM:


    def __init__(self):


        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )


        self.model = Config.LLM_MODEL


        # Tool Router

        self.tool_router = ToolRouter()



    # =====================================
    # Main Generate Function
    # =====================================

    def generate(
        self,
        user_text,
        history=None
    ):


        try:


            logger.info(
                "Generating response..."
            )



            # Tool instruction

            tool_prompt = f"""

You are a helpful AI assistant.

You have access to tools.

Available tools:

{json.dumps(TOOLS_SCHEMA, indent=2)}


Rules:

If a tool is required:
Return ONLY valid JSON.

Example:

{{
 "tool":"get_time",
 "input":null
}}


If no tool is required:
Answer normally.

"""


            messages = [

                {
                    "role":"system",
                    "content":
                    SYSTEM_PROMPT + tool_prompt
                }

            ]



            # Add memory

            if history:


                messages.extend(
                    history
                )



            # Add user

            messages.append(

                {
                    "role":"user",
                    "content":user_text
                }

            )



            # ==============================
            # First LLM Call
            # ==============================


            response = self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                temperature=0.3,

                max_tokens=500

            )



            answer = (

                response
                .choices[0]
                .message
                .content
                .strip()

            )



            # ==============================
            # Check Tool Request
            # ==============================


            tool_request = self.parse_tool_request(
                answer
            )



            if tool_request:



                logger.info(
                    f"Tool requested: {tool_request}"
                )



                tool_name = tool_request.get(
                    "tool"
                )


                tool_input = tool_request.get(
                    "input"
                )



                # Execute tool


                tool_result = self.tool_router.execute(

                    tool_name,

                    tool_input

                )



                logger.info(
                    f"Tool result: {tool_result}"
                )



                # Add previous AI JSON

                messages.append(

                    {
                        "role":"assistant",
                        "content":answer
                    }

                )



                # Add tool response

                messages.append(

                    {

                        "role":"system",

                        "content":
                        f"""

Tool result:

{tool_result}


Now answer the user naturally.

"""

                    }

                )



                # ==============================
                # Final LLM Response
                # ==============================


                final_response = self.client.chat.completions.create(

                    model=self.model,

                    messages=messages,

                    temperature=0.7,

                    max_tokens=500

                )


                answer = (

                    final_response
                    .choices[0]
                    .message
                    .content

                )



            logger.info(
                "Response generated"
            )


            return answer




        except Exception as e:


            logger.error(
                f"LLM failed: {e}"
            )


            return None





    # =====================================
    # Parse Tool JSON
    # =====================================


    def parse_tool_request(
        self,
        text
    ):


        try:


            # Remove markdown

            text = (
                text
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )



            data = json.loads(
                text
            )



            if isinstance(data, dict):


                if "tool" in data:


                    return data



        except Exception:


            pass



        return None