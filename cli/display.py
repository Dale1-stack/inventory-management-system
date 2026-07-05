"""
Display utilities for the Inventory Management CLI.
"""

from typing import Dict, List, Optional

LINE = "=" * 70
SEPARATOR = "-" * 70


def print_header(title: str) -> None:
    print(f"\n{LINE}")
    print(title.center(70))
    print(LINE)


def print_item(item: Dict) -> None:
    """Display a single inventory item."""

    if not item:
        print("\nNo item to display.\n")
        return

    print_header("Inventory Item")

    print(f"ID           : {item.get('id')}")
    print(f"Product Name : {item.get('product_name')}")
    print(f"Brand        : {item.get('brand')}")
    print(f"Barcode      : {item.get('barcode', 'N/A')}")
    print(f"Ingredients  : {item.get('ingredients', 'N/A')}")
    print(f"Stock        : {item.get('stock')}")
    print(f"Price        : KES {float(item.get('price', 0)):.2f}")

    print(LINE)


def print_items(items: List[Dict]) -> None:
    """Display all inventory items."""

    if not items:
        print("\nNo inventory items found.\n")
        return

    print_header("Inventory")

    print(
        "{:<5} {:<30} {:<18} {:>8} {:>12}".format(
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
            "{:<5} {:<30} {:<18} {:>8} {:>12}".format(
                item.get("id"),
                item.get("product_name", "")[:30],
                item.get("brand", "")[:18],
                item.get("stock", 0),
                f"KES {float(item.get('price', 0)):.2f}",
            )
        )

    print(LINE)
    print(f"Total products: {len(items)}")
    print(LINE)


def print_product(product: Optional[Dict]) -> None:
    """Display OpenFoodFacts product information."""

    if not product:
        print("\nProduct not found.\n")
        return

    print_header("OpenFoodFacts Product")

    print(f"Product Name : {product.get('product_name', 'Unknown')}")
    print(f"Brand        : {product.get('brand', 'Unknown')}")
    print(f"Barcode      : {product.get('barcode', 'Unknown')}")
    print(f"Categories   : {product.get('categories', 'Unknown')}")
    print(f"Quantity     : {product.get('quantity', 'Unknown')}")
    print(f"Ingredients  : {product.get('ingredients', 'Unknown')}")
    print(f"NutriScore   : {product.get('nutriscore', 'Unknown')}")

    image = product.get("image")

    if image:
        print(f"Image URL    : {image}")

    print(LINE)


def print_success(message: str) -> None:
    print(f"\n✓ {message}\n")


def print_error(message: str) -> None:
    print(f"\n✗ {message}\n")


def print_warning(message: str) -> None:
    print(f"\n! {message}\n")


def print_info(message: str) -> None:
    print(f"\n> {message}\n")