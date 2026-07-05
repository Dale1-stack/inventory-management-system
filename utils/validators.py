# validators
"""
Validation utilities.
"""


def validate_inventory(data):
    """
    Validate inventory payload.

    Returns:
        (bool, str)
    """

    required_fields = [
        "product_name",
        "brand",
        "price",
        "stock",
    ]

    for field in required_fields:
        if field not in data:
            return False, f"{field} is required."

    if not isinstance(data["product_name"], str):
        return False, "product_name must be a string."

    if not data["product_name"].strip():
        return False, "product_name cannot be empty."

    if not isinstance(data["brand"], str):
        return False, "brand must be a string."

    if not data["brand"].strip():
        return False, "brand cannot be empty."

    if not isinstance(data["price"], (int, float)):
        return False, "price must be numeric."

    if data["price"] < 0:
        return False, "price cannot be negative."

    if not isinstance(data["stock"], int):
        return False, "stock must be an integer."

    if data["stock"] < 0:
        return False, "stock cannot be negative."

    return True, ""