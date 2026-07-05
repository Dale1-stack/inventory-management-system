"""
Unit tests for services.openfoodfacts

All external HTTP requests are mocked.
"""

from unittest.mock import Mock, patch

import requests

from services.openfoodfacts import OpenFoodFactsService


class TestOpenFoodFactsService:
    """Tests for OpenFoodFactsService."""

    ####################################################################
    # NORMALIZATION
    ####################################################################

    def test_normalize_product(self):
        """Test product normalization."""

        raw = {
            "code": "1234567890123",
            "product_name": "Milk",
            "brands": "Brookside",
            "ingredients_text": "Milk, Sugar",
            "categories": "Dairy",
            "quantity": "500ml",
            "image_url": "https://example.com/image.jpg",
            "nutriscore_grade": "a",
        }

        normalized = OpenFoodFactsService._normalize_product(raw)

        assert normalized["barcode"] == "1234567890123"
        assert normalized["product_name"] == "Milk"
        assert normalized["brand"] == "Brookside"
        assert normalized["ingredients"] == "Milk, Sugar"
        assert normalized["categories"] == "Dairy"
        assert normalized["quantity"] == "500ml"
        assert normalized["image"] == "https://example.com/image.jpg"
        assert normalized["nutriscore"] == "a"

    ####################################################################
    # BARCODE SEARCH
    ####################################################################

    @patch("services.openfoodfacts.requests.get")
    def test_search_by_barcode_success(self, mock_get):
        """Successful barcode lookup."""

        response = Mock()

        response.raise_for_status.return_value = None

        response.json.return_value = {
            "status": 1,
            "product": {
                "code": "1234567890123",
                "product_name": "Milk",
                "brands": "Brookside",
                "ingredients_text": "Milk",
            },
        }

        mock_get.return_value = response

        product = OpenFoodFactsService.search_by_barcode(
            "1234567890123"
        )

        assert product is not None
        assert product["barcode"] == "1234567890123"
        assert product["product_name"] == "Milk"

    @patch("services.openfoodfacts.requests.get")
    def test_barcode_not_found(self, mock_get):
        """Unknown barcode."""

        response = Mock()

        response.raise_for_status.return_value = None

        response.json.return_value = {
            "status": 0
        }

        mock_get.return_value = response

        assert (
            OpenFoodFactsService.search_by_barcode(
                "000000"
            )
            is None
        )

    @patch("services.openfoodfacts.requests.get")
    def test_barcode_timeout(self, mock_get):
        """Timeout."""

        mock_get.side_effect = requests.Timeout

        result = OpenFoodFactsService.search_by_barcode(
            "123"
        )

        assert "error" in result
        assert result["error"] == "Request timed out"

    @patch("services.openfoodfacts.requests.get")
    def test_barcode_connection_error(self, mock_get):
        """Connection failure."""

        mock_get.side_effect = requests.ConnectionError

        result = OpenFoodFactsService.search_by_barcode(
            "123"
        )

        assert "error" in result

    @patch("services.openfoodfacts.requests.get")
    def test_barcode_http_error(self, mock_get):
        """HTTP failure."""

        response = Mock()

        response.raise_for_status.side_effect = (
            requests.HTTPError()
        )

        mock_get.return_value = response

        result = OpenFoodFactsService.search_by_barcode(
            "123"
        )

        assert "error" in result

    ####################################################################
    # PRODUCT SEARCH
    ####################################################################

    @patch("services.openfoodfacts.requests.get")
    def test_search_by_name_success(self, mock_get):
        """Successful product search."""

        response = Mock()

        response.raise_for_status.return_value = None

        response.json.return_value = {
            "products": [
                {
                    "code": "1",
                    "product_name": "Milk",
                    "brands": "Brand A",
                },
                {
                    "code": "2",
                    "product_name": "Chocolate Milk",
                    "brands": "Brand B",
                },
            ]
        }

        mock_get.return_value = response

        products = OpenFoodFactsService.search_by_name(
            "milk"
        )

        assert len(products) == 2
        assert products[0]["product_name"] == "Milk"

    @patch("services.openfoodfacts.requests.get")
    def test_search_by_name_empty(self, mock_get):
        """No products returned."""

        response = Mock()

        response.raise_for_status.return_value = None

        response.json.return_value = {
            "products": []
        }

        mock_get.return_value = response

        products = OpenFoodFactsService.search_by_name(
            "xyz"
        )

        assert products == []

    @patch("services.openfoodfacts.requests.get")
    def test_search_by_name_timeout(self, mock_get):
        """Timeout should return empty list."""

        mock_get.side_effect = requests.Timeout

        assert (
            OpenFoodFactsService.search_by_name(
                "milk"
            )
            == []
        )

    ####################################################################
    # INVENTORY CONVERSION
    ####################################################################

    def test_to_inventory_product(self):
        """Convert OpenFoodFacts product."""

        product = {
            "barcode": "123456",
            "product_name": "Milk",
            "brand": "Brookside",
            "ingredients": "Milk",
        }

        inventory = (
            OpenFoodFactsService.to_inventory_product(
                product
            )
        )

        assert inventory["barcode"] == "123456"
        assert inventory["product_name"] == "Milk"
        assert inventory["brand"] == "Brookside"
        assert inventory["ingredients"] == "Milk"
        assert inventory["price"] == 0
        assert inventory["stock"] == 0

    def test_to_inventory_product_none(self):
        """None input should return None."""

        assert (
            OpenFoodFactsService.to_inventory_product(
                None
            )
            is None
        )

    ####################################################################
    # REQUEST VALIDATION
    ####################################################################

    @patch("services.openfoodfacts.requests.get")
    def test_requests_called(self, mock_get):
        """Verify requests.get() is invoked."""

        response = Mock()

        response.raise_for_status.return_value = None

        response.json.return_value = {
            "status": 0
        }

        mock_get.return_value = response

        OpenFoodFactsService.search_by_barcode(
            "737628064502"
        )

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert "737628064502" in args[0]
        assert kwargs["timeout"] == OpenFoodFactsService.TIMEOUT