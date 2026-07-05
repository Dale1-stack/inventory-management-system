"""
Inventory API Routes
"""

from flask import Blueprint, request  # type: ignore[import]

from services.inventory_service import InventoryService
from utils.responses import success, error
from utils.validators import validate_inventory
from utils.logger import logger
from services.openfoodfacts import OpenFoodFactsService

inventory_bp = Blueprint(
    "inventory",
    __name__
)

############################################################
# GET ALL INVENTORY
############################################################

@inventory_bp.route(
    "/inventory",
    methods=["GET"]
)
def get_inventory():

    ########################################################
    # Query Parameters
    ########################################################

    brand = request.args.get("brand")

    product_name = request.args.get(
        "product_name"
    )

    min_price = request.args.get(
        "min_price",
        type=float
    )

    max_price = request.args.get(
        "max_price",
        type=float
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    limit = request.args.get(
        "limit",
        default=10,
        type=int
    )

    ########################################################
    # Business Logic
    ########################################################

    items = InventoryService.filter_inventory(

        brand=brand,

        product_name=product_name,

        min_price=min_price,

        max_price=max_price

    )

    result = InventoryService.paginate(

        items,

        page,

        limit

    )

    logger.info(
        "Inventory retrieved"
    )

    return success(

        "Inventory retrieved",

        result

    )

############################################################
# GET ONE INVENTORY ITEM
############################################################

@inventory_bp.route(
    "/inventory/<int:item_id>",
    methods=["GET"]
)
def get_inventory_item(item_id):

    item = InventoryService.get_by_id(
        item_id
    )

    if not item:

        logger.warning(
            f"Inventory item "
            f"{item_id} not found"
        )

        return error(

            "Inventory item not found",

            404

        )

    logger.info(

        f"Retrieved inventory "

        f"{item_id}"

    )

    return success(

        "Inventory item retrieved",

        item

    )

############################################################
# CREATE INVENTORY ITEM
############################################################

@inventory_bp.route(
    "/inventory",
    methods=["POST"]
)
def create_inventory_item():

    data = request.get_json()

    if data is None:
        return error(
            "Request body must be valid JSON.",
            400
        )

    valid, message = validate_inventory(data)

    if not valid:
        logger.warning(f"Validation failed: {message}")
        return error(message, 400)

    # Prevent duplicate barcode (if provided)
    barcode = data.get("barcode")

    if barcode:
        existing = InventoryService.get_by_barcode(barcode)

        if existing:
            return error(
                "A product with this barcode already exists.",
                409
            )

    created = InventoryService.add(data)

    logger.info(
        f"Created inventory item {created['id']}"
    )

    return success(
        "Inventory item created successfully.",
        created,
        201
    )

############################################################
# UPDATE INVENTORY ITEM
############################################################

@inventory_bp.route(
    "/inventory/<int:item_id>",
    methods=["PATCH"]
)
def update_inventory_item(item_id):

    existing = InventoryService.get_by_id(item_id)

    if existing is None:

        return error(
            "Inventory item not found.",
            404
        )

    updates = request.get_json()

    if updates is None:

        return error(
            "Request body must contain JSON.",
            400
        )

    allowed_fields = {
        "barcode",
        "product_name",
        "brand",
        "ingredients",
        "price",
        "stock",
    }

    invalid_fields = (
        set(updates.keys()) - allowed_fields
    )

    if invalid_fields:

        return error(
            f"Invalid field(s): "
            f"{', '.join(sorted(invalid_fields))}",
            400
        )

    # Validate numeric values
    if "price" in updates:

        if (
            not isinstance(
                updates["price"],
                (int, float)
            )
            or updates["price"] < 0
        ):
            return error(
                "Price must be a non-negative number.",
                400
            )

    if "stock" in updates:

        if (
            not isinstance(
                updates["stock"],
                int
            )
            or updates["stock"] < 0
        ):
            return error(
                "Stock must be a non-negative integer.",
                400
            )

    # Prevent duplicate barcode
    if "barcode" in updates:

        duplicate = InventoryService.get_by_barcode(
            updates["barcode"]
        )

        if (
            duplicate
            and duplicate["id"] != item_id
        ):
            return error(
                "Barcode already exists.",
                409
            )

    updated = InventoryService.update(
        item_id,
        updates
    )

    logger.info(
        f"Updated inventory item {item_id}"
    )

    return success(
        "Inventory item updated successfully.",
        updated
    )

############################################################
# DELETE INVENTORY ITEM
############################################################

@inventory_bp.route(
    "/inventory/<int:item_id>",
    methods=["DELETE"]
)
def delete_inventory_item(item_id):

    deleted = InventoryService.delete(item_id)

    if not deleted:

        logger.warning(
            f"Delete failed for item {item_id}"
        )

        return error(
            "Inventory item not found.",
            404
        )

    logger.info(
        f"Deleted inventory item {item_id}"
    )

    return success(
        "Inventory item deleted successfully."
    )

############################################################
# SEARCH OPENFOODFACTS BY BARCODE
############################################################

@inventory_bp.route(
    "/inventory/search/barcode/<string:barcode>",
    methods=["GET"]
)
def search_product_by_barcode(barcode):

    logger.info(
        f"Searching OpenFoodFacts for barcode: {barcode}"
    )

    product = (
        OpenFoodFactsService.search_by_barcode(
            barcode
        )
    )

    if product is None:

        return error(
            "Product not found.",
            404
        )

    if (
        isinstance(product, dict)
        and "error" in product
    ):

        logger.error(product["error"])

        return error(
            product["error"],
            500
        )

    return success(
        "Product found.",
        product
    )

############################################################
# SEARCH OPENFOODFACTS BY PRODUCT NAME
############################################################

@inventory_bp.route(
    "/inventory/search/name/<string:name>",
    methods=["GET"]
)
def search_product_by_name(name):

    logger.info(
        f"Searching products: {name}"
    )

    products = (
        OpenFoodFactsService.search_by_name(
            name
        )
    )

    if len(products) == 0:

        return error(
            "No matching products found.",
            404
        )

    return success(
        "Products retrieved successfully.",
        {
            "count": len(products),
            "products": products
        }
    )

############################################################
# IMPORT PRODUCT FROM OPENFOODFACTS
############################################################

@inventory_bp.route(
    "/inventory/import/<string:barcode>",
    methods=["POST"]
)
def import_product(barcode):

    logger.info(
        f"Import request for barcode: {barcode}"
    )

    # Check if product already exists
    existing = InventoryService.get_by_barcode(barcode)

    if existing:

        return error(
            "Product already exists in inventory.",
            409
        )

    product = (
        OpenFoodFactsService.search_by_barcode(
            barcode
        )
    )

    if product is None:

        return error(
            "Product not found.",
            404
        )

    if (
        isinstance(product, dict)
        and "error" in product
    ):

        logger.error(product["error"])

        return error(
            product["error"],
            500
        )

    inventory_product = (
        OpenFoodFactsService.to_inventory_product(
            product
        )
    )

    created = InventoryService.add(
        inventory_product
    )

    logger.info(
        f"Imported product {created['id']}"
    )

    return success(
        "Product imported successfully.",
        created,
        201
    )

############################################################
# ENRICH INVENTORY ITEM
############################################################

@inventory_bp.route(
    "/inventory/enriched/<int:item_id>",
    methods=["GET"]
)
def enriched_inventory_item(item_id):

    item = InventoryService.get_by_id(
        item_id
    )

    if item is None:

        return error(
            "Inventory item not found.",
            404
        )

    barcode = item.get("barcode")

    if not barcode:

        return success(
            "Inventory item retrieved.",
            {
                **item,
                "live_data": None
            }
        )

    api_product = (
        OpenFoodFactsService.search_by_barcode(
            barcode
        )
    )

    if (
        api_product is None
        or (
            isinstance(api_product, dict)
            and "error" in api_product
        )
    ):

        enriched = {
            **item,
            "live_data": None
        }

    else:

        enriched = {
            **item,
            "live_data": api_product
        }

    logger.info(
        f"Enriched inventory item {item_id}"
    )

    return success(
        "Enriched inventory item retrieved.",
        enriched
    )

