"""
Logging configuration.
"""

import logging
import os

from config import Config


def configure_logging():
    """
    Configure application logging.
    """

    os.makedirs(Config.LOG_FOLDER, exist_ok=True)

    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    return logging.getLogger("inventory")


logger = configure_logging()