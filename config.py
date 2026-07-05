"""
Application Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    #######################################################
    # Flask
    #######################################################

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "inventory-secret-key"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    #######################################################
    # API
    #######################################################

    OPENFOODFACTS_URL = (
        "https://world.openfoodfacts.org"
    )

    REQUEST_TIMEOUT = 5

    #######################################################
    # Pagination
    #######################################################

    DEFAULT_PAGE_SIZE = 10

    MAX_PAGE_SIZE = 50

    #######################################################
    # Logging
    #######################################################

    LOG_FOLDER = "logs"

    LOG_FILE = "logs/app.log"