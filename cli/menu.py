"""
CLI menu actions for the Inventory Management System.
"""

try:
    from .api_client import (
        get_items,
        get_item,
        create_item,
        update_item_api,
        delete_item_api,
        fetch_openfoodfacts,
        import_product_api,
        get_enriched_item,
    )

    from .display import (
        print_item,
        print_items,
        print_product,
    )
except ImportError:  # pragma: no cover - fallback for direct script execution
    from cli.api_client import (
        get_items,
        get_item,
        create_item,
        update_item_api,
        delete_item_api,
        fetch_openfoodfacts,
    )

    from cli.display import (
        print_item,
        print_items,
        print_product,
    )


def main_menu():
    """Display the main menu and return the user's choice."""
    print("\n" + "=" * 50)
    print("      INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. View all inventory items")
    print("2. View a single inventory item")
    print("3. Add inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Fetch product from OpenFoodFacts")
    print("7. Import product from OpenFoodFacts")
    print("8. View enriched inventory item")
    print("0. Exit")
    print("=" * 60)

    return input("Select an option: ").strip()


def view_all_items():
    """Display all inventory items."""

    data = get_items()

    if not data:
        print("\nNo inventory items found.")
        return

    print_items(data.get("items", []))
def search_item():
    """Display a single inventory item."""

    try:
        item_id = int(input("Enter item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    item = get_item(item_id)

    if item is None:
        print("Item not found.")
        return

    print_item(item)

def add_item():
    """Create a new inventory item."""

    print("\nAdd Inventory Item\n")

    payload = {
        "product_name": input("Product Name: ").strip(),
        "brand": input("Brand: ").strip(),
        "barcode": input("Barcode: ").strip(),
        "ingredients": input("Ingredients: ").strip(),
    }

    try:
        payload["stock"] = int(input("Stock: ").strip())

        price_input = input("Price: ").strip()
        price_input = price_input.replace("$", "")

        payload["price"] = float(price_input)

    except ValueError:
        print("Stock must be an integer and price must be a valid number.")
        return

    created = create_item(payload)

    print("\nItem created successfully.\n")
    print_item(created)

def update_item():
    """Update an inventory item."""

    try:
        item_id = int(input("Item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    existing = get_item(item_id)

    if existing is None:
        print("Item not found.")
        return

    print("\nLeave blank to keep existing values.\n")

    payload = {}

    product_name = input(
        f"Product Name [{existing['product_name']}]: "
    ).strip()

    if product_name:
        payload["product_name"] = product_name

    brand = input(
        f"Brand [{existing['brand']}]: "
    ).strip()

    if brand:
        payload["brand"] = brand

    barcode = input(
        f"Barcode [{existing['barcode']}]: "
    ).strip()

    if barcode:
        payload["barcode"] = barcode

    ingredients = input(
        f"Ingredients [{existing.get('ingredients','')}]: "
    ).strip()

    if ingredients:
        payload["ingredients"] = ingredients

    stock = input(
        f"Stock [{existing['stock']}]: "
    ).strip()

    if stock:
        payload["stock"] = int(stock)

    price = input(
        f"Price [{existing['price']}]: "
    ).strip()

    if price:
        payload["price"] = float(price)

    updated = update_item_api(
        item_id,
        payload,
    )

    print("\nUpdated successfully.\n")
    print_item(updated)

def delete_item():
    """Delete an inventory item."""

    try:
        item_id = int(input("Item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input(
        "Delete this item? (y/n): "
    ).lower()

    if confirm != "y":
        print("Cancelled.")
        return

    delete_item_api(item_id)

    print("\nItem deleted successfully.")


def fetch_product():
    """Search OpenFoodFacts."""

    query = input(
        "\nBarcode or Product Name: "
    ).strip()

    if not query:
        return

    result = fetch_openfoodfacts(query)

    if query.isdigit():
        print_product(result)
    else:
        products = result.get("products", [])

        if not products:
            print("No products found.")
            return

        for i, product in enumerate(products, start=1):
            print(
                f"{i}. "
                f"{product['product_name']} "
                f"({product['brand']})"
            )

        choice = int(
            input("\nChoose product: ")
        )

        print_product(
            products[choice - 1]
        )

def import_product():
    """Import a product into inventory."""

    barcode = input(
        "\nBarcode: "
    ).strip()

    if not barcode:
        return

    item = import_product_api(barcode)

    print("\nImported successfully.\n")
    print_item(item)

def enriched_item():
    """Display inventory item with OpenFoodFacts data."""

    try:
        item_id = int(
            input("\nInventory ID: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    item = get_enriched_item(item_id)

    print("\nInventory Item")
    print_item(item)

    if item.get("live_data"):
        print("\nLive OpenFoodFacts Data")
        print_product(item["live_data"])
    else:
        print("\nNo OpenFoodFacts data available.")