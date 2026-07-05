"""
Integration tests for the Inventory API routes.
"""

from unittest.mock import patch


class TestInventoryRoutes:
    """Tests for inventory endpoints."""

    ####################################################################
    # HOME
    ####################################################################

    def test_home_route(self, client):
        response = client.get("/")

        assert response.status_code == 200

        data = response.get_json()

        assert data["application"] == "Inventory Management API"

    ####################################################################
    # GET INVENTORY
    ####################################################################

    def test_get_inventory(self, client):
        response = client.get("/inventory")

        assert response.status_code == 200

        body = response.get_json()

        assert body["success"] is True
        assert "data" in body
        assert "items" in body["data"]

    def test_get_inventory_with_brand_filter(self, client):
        response = client.get("/inventory?brand=Ferrero")

        assert response.status_code == 200

        items = response.get_json()["data"]["items"]

        assert len(items) == 1
        assert items[0]["brand"] == "Ferrero"

    ####################################################################
    # GET SINGLE ITEM
    ####################################################################

    def test_get_existing_item(self, client):
        response = client.get("/inventory/1")

        assert response.status_code == 200

        body = response.get_json()

        assert body["success"] is True
        assert body["data"]["id"] == 1

    def test_get_missing_item(self, client):
        response = client.get("/inventory/9999")

        assert response.status_code == 404

        assert response.get_json()["success"] is False

    ####################################################################
    # CREATE
    ####################################################################

    def test_create_inventory_item(self, client):

        payload = {
            "barcode": "9999999999999",
            "product_name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 15,
            "ingredients": "Sugar",
        }

        response = client.post(
            "/inventory",
            json=payload,
        )

        assert response.status_code == 201

        body = response.get_json()

        assert body["success"] is True
        assert body["data"]["product_name"] == "Test Product"

    def test_create_duplicate_barcode(self, client):

        payload = {
            "barcode": "737628064502",
            "product_name": "Duplicate",
            "brand": "Brand",
            "price": 10,
            "stock": 2,
        }

        response = client.post(
            "/inventory",
            json=payload,
        )

        assert response.status_code == 409

    def test_create_invalid_payload(self, client):

        payload = {
            "product_name": "",
            "brand": "",
            "price": -1,
            "stock": -5,
        }

        response = client.post(
            "/inventory",
            json=payload,
        )

        assert response.status_code == 400

    ####################################################################
    # UPDATE
    ####################################################################

    def test_update_inventory_item(self, client):

        payload = {
            "price": 999,
            "stock": 40,
        }

        response = client.patch(
            "/inventory/1",
            json=payload,
        )

        assert response.status_code == 200

        data = response.get_json()["data"]

        assert data["price"] == 999
        assert data["stock"] == 40

    def test_update_missing_item(self, client):

        response = client.patch(
            "/inventory/9999",
            json={"price": 20},
        )

        assert response.status_code == 404

    def test_update_invalid_field(self, client):

        response = client.patch(
            "/inventory/1",
            json={"unknown": "value"},
        )

        assert response.status_code == 400

    def test_update_duplicate_barcode(self, client):

        response = client.patch(
            "/inventory/1",
            json={
                "barcode": "3017620422003"
            },
        )

        assert response.status_code == 409

    ####################################################################
    # DELETE
    ####################################################################

    def test_delete_item(self, client):

        response = client.delete("/inventory/1")

        assert response.status_code == 200

        assert response.get_json()["success"] is True

    def test_delete_missing_item(self, client):

        response = client.delete("/inventory/9999")

        assert response.status_code == 404

    ####################################################################
    # BARCODE SEARCH
    ####################################################################

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_barcode"
    )
    def test_search_barcode_success(
        self,
        mock_search,
        client,
    ):

        mock_search.return_value = {
            "barcode": "123",
            "product_name": "Milk",
            "brand": "Brookside",
        }

        response = client.get(
            "/inventory/search/barcode/123"
        )

        assert response.status_code == 200

        assert (
            response.get_json()["data"]["product_name"]
            == "Milk"
        )

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_barcode"
    )
    def test_search_barcode_not_found(
        self,
        mock_search,
        client,
    ):

        mock_search.return_value = None

        response = client.get(
            "/inventory/search/barcode/123"
        )

        assert response.status_code == 404

    ####################################################################
    # PRODUCT SEARCH
    ####################################################################

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_name"
    )
    def test_search_name_success(
        self,
        mock_search,
        client,
    ):

        mock_search.return_value = [
            {
                "product_name": "Milk"
            }
        ]

        response = client.get(
            "/inventory/search/name/milk"
        )

        assert response.status_code == 200

        assert (
            response.get_json()["data"]["count"]
            == 1
        )

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_name"
    )
    def test_search_name_not_found(
        self,
        mock_search,
        client,
    ):

        mock_search.return_value = []

        response = client.get(
            "/inventory/search/name/xyz"
        )

        assert response.status_code == 404

    ####################################################################
    # IMPORT PRODUCT
    ####################################################################

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_barcode"
    )
    @patch(
        "routes.inventory_routes.OpenFoodFactsService.to_inventory_product"
    )
    def test_import_product(
        self,
        mock_convert,
        mock_search,
        client,
    ):

        mock_search.return_value = {
            "barcode": "8888888888888",
            "product_name": "Imported",
            "brand": "Brand",
            "ingredients": "",
        }

        mock_convert.return_value = {
            "barcode": "8888888888888",
            "product_name": "Imported",
            "brand": "Brand",
            "ingredients": "",
            "price": 0,
            "stock": 0,
        }

        response = client.post(
            "/inventory/import/8888888888888"
        )

        assert response.status_code == 201

        assert (
            response.get_json()["data"]["barcode"]
            == "8888888888888"
        )

    ####################################################################
    # ENRICH INVENTORY
    ####################################################################

    @patch(
        "routes.inventory_routes.OpenFoodFactsService.search_by_barcode"
    )
    def test_enriched_inventory(
        self,
        mock_search,
        client,
    ):

        mock_search.return_value = {
            "barcode": "737628064502",
            "product_name": "Organic Almond Milk",
        }

        response = client.get(
            "/inventory/enriched/1"
        )

        assert response.status_code == 200

        body = response.get_json()

        assert body["success"] is True
        assert body["data"]["live_data"] is not None

    def test_enriched_missing_item(self, client):

        response = client.get(
            "/inventory/enriched/9999"
        )

        assert response.status_code == 404