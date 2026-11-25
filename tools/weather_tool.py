import requests

from utils.logger import get_logger


logger = get_logger("WEATHER")


def get_weather(city):

    try:

        logger.info(
            f"Getting weather for {city}"
        )


        url = (
            f"https://wttr.in/{city}"
            "?format=%C+%t"
        )


        response = requests.get(
            url,
            timeout=5
        )


        if response.status_code == 200:

            return response.text


        return "Weather unavailable"



    except Exception as e:

        logger.error(
            f"Weather error: {e}"
        )

        return "Unable to get weather"