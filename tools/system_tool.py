import psutil

from utils.logger import get_logger


logger = get_logger("SYSTEM")



def get_system_info():

    try:

        cpu = psutil.cpu_percent()

        memory = psutil.virtual_memory()


        result = {

            "cpu_usage":
            f"{cpu}%",

            "ram_usage":
            f"{memory.percent}%",

            "ram_available":
            f"{round(memory.available / (1024**3),2)} GB"

        }


        logger.info(
            "System info collected"
        )


        return result



    except Exception as e:


        logger.error(
            f"System tool error: {e}"
        )


        return None