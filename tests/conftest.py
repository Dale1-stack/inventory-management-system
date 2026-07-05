"""
Shared pytest fixtures for the Inventory Management System.
"""

from copy import deepcopy

import pytest

from app import create_app
from database.inventory import inventory
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

###############################################################################
# Flask Application
###############################################################################

@pytest.fixture(scope="session")
def app():
    """
    Create the Flask application.
    """
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture()
def client(app):
    """
    Flask test client.
    """
    return app.test_client()


###############################################################################
# Inventory Reset
###############################################################################

# Save the original inventory once
ORIGINAL_INVENTORY = deepcopy(inventory)


@pytest.fixture(autouse=True)
def reset_inventory():
    """
    Reset the in-memory inventory before every test.
    """

    inventory.clear()
    inventory.extend(deepcopy(ORIGINAL_INVENTORY))

    yield

    inventory.clear()
    inventory.extend(deepcopy(ORIGINAL_INVENTORY))

###############################################################################
# Sample Inventory Payloads
###############################################################################

@pytest.fixture
def sample_item():
    """
    Valid inventory item.
    """
    return {
        "barcode": "9999999999999",
        "product_name": "Test Product",
        "brand": "Test Brand",
        "price": 150.00,
        "stock": 10,
        "ingredients": "Sugar, Water",
    }


@pytest.fixture
def second_item():
    """
    Another inventory item.
    """
    return {
        "barcode": "8888888888888",
        "product_name": "Coffee",
        "brand": "Nescafe",
        "price": 350.00,
        "stock": 25,
        "ingredients": "Coffee Beans",
    }


###############################################################################
# Invalid Payloads
###############################################################################

@pytest.fixture
def invalid_item():
    """
    Invalid inventory payload.
    """
    return {
        "product_name": "",
        "brand": "",
        "price": -10,
        "stock": -5,
    }


###############################################################################
# OpenFoodFacts Sample
###############################################################################

@pytest.fixture
def sample_product():
    """
    Sample OpenFoodFacts response after normalization.
    """
    return {
        "barcode": "737628064502",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds",
        "categories": "Plant-based foods",
        "quantity": "1L",
        "image": "https://example.com/image.jpg",
        "nutriscore": "a",
    }