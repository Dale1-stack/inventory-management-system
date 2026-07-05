"""
Inventory Service

Business logic for inventory management.
"""

from copy import deepcopy
from database.inventory import inventory


class InventoryService:

    #########################################################
    # ID GENERATION
    #########################################################

    @staticmethod
    def generate_id():
        """
        Generate the next inventory ID.
        """
        if not inventory:
            return 1

        return max(item["id"] for item in inventory) + 1

    #########################################################
    # GET ALL
    #########################################################

    @staticmethod
    def get_all():
        """
        Return a copy of the inventory list.
        """
        return deepcopy(inventory)

    #########################################################
    # GET BY ID
    #########################################################

    @staticmethod
    def get_by_id(item_id):
        """
        Find an item by ID.
        """
        for item in inventory:
            if item["id"] == item_id:
                return deepcopy(item)

        return None

    #########################################################
    # GET BY BARCODE
    #########################################################

    @staticmethod
    def get_by_barcode(barcode):
        """
        Find an item by barcode.
        """
        for item in inventory:
            if item.get("barcode") == barcode:
                return deepcopy(item)

        return None

    #########################################################
    # ADD ITEM
    #########################################################

    @staticmethod
    def add(item):
        """
        Add a new inventory item.
        """

        new_item = deepcopy(item)

        new_item["id"] = InventoryService.generate_id()

        inventory.append(new_item)

        return deepcopy(new_item)

    #########################################################
    # UPDATE ITEM
    #########################################################

    @staticmethod
    def update(item_id, updates):
        """
        Update an existing inventory item.
        """

        for index, item in enumerate(inventory):

            if item["id"] == item_id:

                inventory[index].update(updates)

                return deepcopy(inventory[index])

        return None

    #########################################################
    # DELETE ITEM
    #########################################################

    @staticmethod
    def delete(item_id):
        """
        Delete an inventory item.
        """

        for index, item in enumerate(inventory):

            if item["id"] == item_id:

                del inventory[index]

                return True

        return False

    #########################################################
    # FILTER INVENTORY
    #########################################################

    @staticmethod
    def filter_inventory(
        brand=None,
        product_name=None,
        min_price=None,
        max_price=None,
    ):
        """
        Filter inventory by various fields.
        """

        results = deepcopy(inventory)

        if brand:
            results = [
                item
                for item in results
                if item["brand"].lower() == brand.lower()
            ]

        if product_name:
            results = [
                item
                for item in results
                if product_name.lower()
                in item["product_name"].lower()
            ]

        if min_price is not None:
            results = [
                item
                for item in results
                if item["price"] >= float(min_price)
            ]

        if max_price is not None:
            results = [
                item
                for item in results
                if item["price"] <= float(max_price)
            ]

        return results

    #########################################################
    # PAGINATION
    #########################################################

    @staticmethod
    def paginate(items, page=1, limit=10):
        """
        Paginate inventory.
        """

        total = len(items)

        start = (page - 1) * limit

        end = start + limit

        return {

            "page": page,

            "limit": limit,

            "total": total,

            "pages": (
                total + limit - 1
            ) // limit,

            "items": items[start:end]

        }

    #########################################################
    # IMPORT PRODUCT
    #########################################################

    @staticmethod
    def import_product(product):
        """
        Import a product from OpenFoodFacts.
        """

        if InventoryService.get_by_barcode(
            product["barcode"]
        ):
            return None

        inventory_item = {

            "barcode":
                product.get("barcode"),

            "product_name":
                product.get("product_name"),

            "brand":
                product.get("brand"),

            "ingredients":
                product.get("ingredients"),

            # Not supplied by OpenFoodFacts
            "price": 0,

            "stock": 0,

        }

        return InventoryService.add(
            inventory_item
        )