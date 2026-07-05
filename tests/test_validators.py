"""
Tests for utils.validators

These tests are written for the validate_inventory() function,
which returns (bool, message) instead of raising exceptions.
"""

import pytest

from utils.validators import validate_inventory


###############################################################################
# Valid Payload
###############################################################################

def test_validate_inventory_success():
    """A valid inventory payload should pass validation."""

    payload = {
        "barcode": "1234567890123",
        "product_name": "Milk",
        "brand": "Brookside",
        "price": 250.50,
        "stock": 20,
        "ingredients": "Milk",
    }

    valid, message = validate_inventory(payload)

    assert valid is True
    assert message == ""


###############################################################################
# Required Fields
###############################################################################

@pytest.mark.parametrize(
    "missing_field",
    [
        "product_name",
        "brand",
        "price",
        "stock",
    ],
)
def test_missing_required_field(missing_field):
    """Missing required fields should fail validation."""

    payload = {
        "product_name": "Milk",
        "brand": "Brookside",
        "price": 250,
        "stock": 10,
    }

    payload.pop(missing_field)

    valid, message = validate_inventory(payload)

    assert valid is False
    assert missing_field in message


###############################################################################
# Product Name Validation
###############################################################################

def test_product_name_must_be_string():

    payload = {
        "product_name": 123,
        "brand": "Brand",
        "price": 100,
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "product_name must be a string" in message


def test_product_name_cannot_be_empty():

    payload = {
        "product_name": "   ",
        "brand": "Brand",
        "price": 100,
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "product_name cannot be empty" in message


###############################################################################
# Brand Validation
###############################################################################

def test_brand_must_be_string():

    payload = {
        "product_name": "Milk",
        "brand": 123,
        "price": 100,
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "brand must be a string" in message


def test_brand_cannot_be_empty():

    payload = {
        "product_name": "Milk",
        "brand": "",
        "price": 100,
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "brand cannot be empty" in message


###############################################################################
# Price Validation
###############################################################################

def test_price_must_be_numeric():

    payload = {
        "product_name": "Milk",
        "brand": "Brand",
        "price": "cheap",
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "price must be numeric" in message


def test_price_cannot_be_negative():

    payload = {
        "product_name": "Milk",
        "brand": "Brand",
        "price": -1,
        "stock": 10,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "price cannot be negative" in message


###############################################################################
# Stock Validation
###############################################################################

def test_stock_must_be_integer():

    payload = {
        "product_name": "Milk",
        "brand": "Brand",
        "price": 100,
        "stock": 10.5,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "stock must be an integer" in message


def test_stock_cannot_be_negative():

    payload = {
        "product_name": "Milk",
        "brand": "Brand",
        "price": 100,
        "stock": -5,
    }

    valid, message = validate_inventory(payload)

    assert valid is False
    assert "stock cannot be negative" in message


###############################################################################
# Boundary Values
###############################################################################

def test_zero_price_is_allowed():

    payload = {
        "product_name": "Free Sample",
        "brand": "Demo",
        "price": 0,
        "stock": 5,
    }

    valid, message = validate_inventory(payload)

    assert valid is True
    assert message == ""


def test_zero_stock_is_allowed():

    payload = {
        "product_name": "Out of Stock Item",
        "brand": "Demo",
        "price": 50,
        "stock": 0,
    }

    valid, message = validate_inventory(payload)

    assert valid is True
    assert message == ""


###############################################################################
# Extra Fields
###############################################################################

def test_extra_fields_are_allowed():
    """
    The validator only checks required fields.
    Additional fields should not cause validation failure.
    """

    payload = {
        "barcode": "123456789",
        "product_name": "Milk",
        "brand": "Brookside",
        "price": 250,
        "stock": 15,
        "ingredients": "Milk",
        "supplier": "Demo Supplier",
        "country": "Kenya",
    }

    valid, message = validate_inventory(payload)

    assert valid is True
    assert message == ""