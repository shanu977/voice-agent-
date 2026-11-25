from router.router import ToolRouter


class ToolManager:


    def __init__(self):

        self.router = ToolRouter()



    def run(
        self,
        tool_name,
        arguments=None
    ):

        return self.router.execute(
            tool_name,
            arguments
        )