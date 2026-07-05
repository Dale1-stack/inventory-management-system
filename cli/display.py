"""
Display utilities for the Inventory Management CLI.
"""

from typing import Dict, List, Optional

LINE = "=" * 80
SEPARATOR = "-" * 80


def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{LINE}")
    print(title.center(80))
    print(LINE)


###########################################################
# SINGLE INVENTORY ITEM
###########################################################

def print_item(item: Dict) -> None:
    """Display one inventory item."""

    if not item:
        print("\nNo item found.\n")
        return

    print_header("Inventory Item")

    print(f"ID           : {item.get('id')}")
    print(f"Product      : {item.get('product_name')}")
    print(f"Brand        : {item.get('brand')}")
    print(f"Barcode      : {item.get('barcode')}")
    print(f"Ingredients  : {item.get('ingredients')}")
    print(f"Stock        : {item.get('stock')}")
    print(f"Price        : ${float(item.get('price', 0)):.2f}")

    print(LINE)


###########################################################
# INVENTORY LIST
###########################################################

def print_items(items: List[Dict]) -> None:
    """Display inventory table."""

    if not items:
        print("\nInventory is empty.\n")
        return

    print_header("Inventory")

    print(
        "{:<4} {:<28} {:<18} {:>8} {:>10}".format(
            "ID",
            "Product",
            "Brand",
            "Stock",
            "Price",
        )
    )

    print(SEPARATOR)

    for item in items:

        print(
            "{:<4} {:<28} {:<18} {:>8} {:>10}".format(
                item.get("id"),
                item.get("product_name", "")[:28],
                item.get("brand", "")[:18],
                item.get("stock"),
                f"${item.get('price',0):.2f}",
            )
        )

    print(SEPARATOR)
    print(f"Total inventory items: {len(items)}")
    print(LINE)


###########################################################
# OPENFOODFACTS PRODUCT
###########################################################

def print_product(product: Optional[Dict]) -> None:
    """Display OpenFoodFacts product."""

    if not product:
        print("\nProduct not found.\n")
        return

    print_header("OpenFoodFacts Product")

    print(f"Product      : {product.get('product_name')}")
    print(f"Brand        : {product.get('brand')}")
    print(f"Barcode      : {product.get('barcode')}")
    print(f"Ingredients  : {product.get('ingredients')}")
    print(f"Categories   : {product.get('categories')}")
    print(f"Quantity     : {product.get('quantity')}")
    print(f"NutriScore   : {product.get('nutriscore')}")

    if product.get("image"):
        print(f"Image        : {product['image']}")

    print(LINE)


###########################################################
# MESSAGES
###########################################################

def print_success(message: str):
    print(f"\n✓ {message}\n")


def print_error(message: str):
    print(f"\n✗ {message}\n")


def print_warning(message: str):
    print(f"\n! {message}\n")


def print_info(message: str):
    print(f"\n> {message}\n")