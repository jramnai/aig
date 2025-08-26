import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # Keep console output too
    ],
)

logger = logging.getLogger(__name__)
