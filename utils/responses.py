"""
Standard JSON response helpers.
"""

from flask import jsonify


def success(message, data=None, status_code=200):
    """
    Success response.
    """
    return (
        jsonify(
            {
                "success": True,
                "message": message,
                "data": data,
            }
        ),
        status_code,
    )


def error(message, status_code=400):
    """
    Error response.
    """
    return (
        jsonify(
            {
                "success": False,
                "message": message,
            }
        ),
        status_code,
    )