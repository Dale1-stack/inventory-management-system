"""
Unit tests for the InventoryService.

These tests target the in-memory inventory implementation.
"""

from copy import deepcopy

from database.inventory import inventory
from services.inventory_service import InventoryService


class TestInventoryService:
    """Tests for InventoryService."""

    ####################################################################
    # GET ALL
    ####################################################################

    def test_get_all_returns_list(self):
        items = InventoryService.get_all()

        assert isinstance(items, list)
        assert len(items) == len(inventory)

    def test_get_all_returns_copy(self):
        items = InventoryService.get_all()

        items.clear()

        assert len(inventory) > 0

    ####################################################################
    # GET BY ID
    ####################################################################

    def test_get_by_id_existing(self):
        item = InventoryService.get_by_id(1)

        assert item is not None
        assert item["id"] == 1

    def test_get_by_id_missing(self):
        assert InventoryService.get_by_id(9999) is None

    ####################################################################
    # GET BY BARCODE
    ####################################################################

    def test_get_by_barcode_existing(self):
        barcode = inventory[0]["barcode"]

        item = InventoryService.get_by_barcode(barcode)

        assert item is not None
        assert item["barcode"] == barcode

    def test_get_by_barcode_missing(self):
        assert (
            InventoryService.get_by_barcode(
                "0000000000000"
            )
            is None
        )

    ####################################################################
    # ADD
    ####################################################################

    def test_add_inventory_item(self, sample_item):
        original_count = len(inventory)

        created = InventoryService.add(sample_item)

        assert created["id"] == original_count + 1
        assert created["product_name"] == sample_item["product_name"]

        assert len(inventory) == original_count + 1

    def test_add_does_not_modify_original_object(
        self,
        sample_item,
    ):
        original = deepcopy(sample_item)

        InventoryService.add(sample_item)

        assert sample_item == original

    ####################################################################
    # UPDATE
    ####################################################################

    def test_update_existing_item(self):
        updated = InventoryService.update(
            1,
            {
                "price": 999,
                "stock": 50,
            },
        )

        assert updated is not None
        assert updated["price"] == 999
        assert updated["stock"] == 50

    def test_update_product_name(self):
        updated = InventoryService.update(
            1,
            {
                "product_name": "Updated Product"
            },
        )

        assert updated["product_name"] == "Updated Product"

    def test_update_missing_item(self):
        result = InventoryService.update(
            9999,
            {"price": 10},
        )

        assert result is None

    ####################################################################
    # DELETE
    ####################################################################

    def test_delete_existing_item(self):
        original = len(inventory)

        deleted = InventoryService.delete(1)

        assert deleted is True
        assert len(inventory) == original - 1

    def test_delete_missing_item(self):
        assert InventoryService.delete(99999) is False

    ####################################################################
    # FILTERING
    ####################################################################

    def test_filter_by_brand(self):
        results = InventoryService.filter_inventory(
            brand="Ferrero"
        )

        assert len(results) == 1
        assert results[0]["brand"] == "Ferrero"

    def test_filter_by_product_name(self):
        results = InventoryService.filter_inventory(
            product_name="Nutella"
        )

        assert len(results) == 1

    def test_filter_by_min_price(self):
        results = InventoryService.filter_inventory(
            min_price=600
        )

        assert all(
            item["price"] >= 600
            for item in results
        )

    def test_filter_by_max_price(self):
        results = InventoryService.filter_inventory(
            max_price=150
        )

        assert all(
            item["price"] <= 150
            for item in results
        )

    def test_filter_no_results(self):
        results = InventoryService.filter_inventory(
            brand="Unknown Brand"
        )

        assert results == []

    ####################################################################
    # PAGINATION
    ####################################################################

    def test_paginate_first_page(self):
        items = InventoryService.get_all()

        page = InventoryService.paginate(
            items,
            page=1,
            limit=5,
        )

        assert page["page"] == 1
        assert page["limit"] == 5
        assert page["total"] == len(items)
        assert len(page["items"]) == 5

    def test_paginate_second_page(self):
        items = InventoryService.get_all()

        page = InventoryService.paginate(
            items,
            page=2,
            limit=5,
        )

        assert page["page"] == 2
        assert len(page["items"]) == 5

    ####################################################################
    # IMPORT PRODUCT
    ####################################################################

    def test_import_product(self, sample_product):
        original = len(inventory)

        created = InventoryService.import_product(
            sample_product
        )

        assert created is not None
        assert created["barcode"] == sample_product["barcode"]
        assert len(inventory) == original + 1

    def test_import_duplicate_product(self):
        product = {
            "barcode": inventory[0]["barcode"],
            "product_name": "Duplicate",
            "brand": "Brand",
            "ingredients": "",
        }

        created = InventoryService.import_product(
            product
        )

        assert created is None

    ####################################################################
    # ID GENERATION
    ####################################################################

    def test_generate_id(self):
        expected = max(
            item["id"] for item in inventory
        ) + 1

        assert (
            InventoryService.generate_id()
            == expected
        )