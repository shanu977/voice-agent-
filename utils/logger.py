import logging
import os


# ======================================
# Logs Directory
# ======================================

LOG_DIR = "logs"


os.makedirs(
    LOG_DIR,
    exist_ok=True
)



# ======================================
# Log File
# ======================================

LOG_FILE = os.path.join(
    LOG_DIR,
    "voice_agent.log"
)



# ======================================
# Logging Configuration
# ======================================

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),


        logging.StreamHandler()

    ]

)




# ======================================
# Logger Factory
# ======================================

def get_logger(name: str):

    """
    Create module specific logger

    Example:

        logger = get_logger("LLM")

        logger.info("Model loaded")

    """

    logger = logging.getLogger(name)


    return logger