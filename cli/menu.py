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
    print("0. Exit")
    print("=" * 50)

    return input("Select an option: ").strip()


def view_all_items():
    """Display all inventory items."""
    response = get_items()

    if not response:
        print("\nNo inventory items found.")
        return

    items = response.get("items", [])

    print_items(items)
def search_item():
    """Display a single inventory item."""
    try:
        item_id = int(input("Enter item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    item = get_item(item_id)

    if not item:
        print("Item not found.")
        return

    print_item(item)

def add_item():
    """Prompt user for a new inventory item."""

    print("\nAdd Inventory Item\n")

    product_name = input("Product Name: ").strip()
    brand = input("Brand: ").strip()
    barcode = input("Barcode: ").strip()
    ingredients = input("Ingredients: ").strip()

    try:
        stock = int(input("Stock: "))
        price = float(input("Price: "))
    except ValueError:
        print("Stock must be an integer and price must be a number.")
        return

    payload = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "ingredients": ingredients,
        "stock": stock,
        "price": price,
    }

    item = create_item(payload)

    if item:
        print("\nItem created successfully.\n")
        print_item(item)
    else:
        print("Failed to create item.")

def update_item():
    """Update an inventory item."""

    try:
        item_id = int(input("Item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    existing = get_item(item_id)

    if not existing:
        print("Item not found.")
        return

    print("\nLeave blank to keep the current value.\n")

    product_name = input(
        f"Product Name [{existing['product_name']}]: "
    ).strip()

    brand = input(
        f"Brand [{existing['brand']}]: "
    ).strip()

    barcode = input(
        f"Barcode [{existing['barcode']}]: "
    ).strip()

    ingredients = input(
        f"Ingredients [{existing.get('ingredients','')}]: "
    ).strip()

    stock = input(
        f"Stock [{existing['stock']}]: "
    ).strip()

    price = input(
        f"Price [{existing['price']}]: "
    ).strip()

    payload = {}

    if product_name:
        payload["product_name"] = product_name

    if brand:
        payload["brand"] = brand

    if barcode:
        payload["barcode"] = barcode

    if ingredients:
        payload["ingredients"] = ingredients

    if stock:
        payload["stock"] = int(stock)

    if price:
        payload["price"] = float(price)

    updated = update_item_api(
        item_id,
        payload
    )

    if updated:
        print("\nItem updated successfully.\n")
        print_item(updated)
    else:
        print("Update failed.")


def delete_item():
    """Delete an inventory item."""
    try:
        item_id = int(input("Item ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input(
        "Are you sure? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    if delete_item_api(item_id):
        print("Item deleted successfully.")
    else:
        print("Delete failed.")


def fetch_product():
    """Fetch product details from OpenFoodFacts."""

    query = input("\nEnter barcode or product name: ").strip()

    if not query:
        print("Query cannot be empty.")
        return

    result = fetch_openfoodfacts(query)

    if not result:
        print("Product not found.")
        return

    # Name search returns multiple products
    if isinstance(result, dict) and "products" in result:
        products = result["products"]

        if not products:
            print("No matching products found.")
            return

        print("\nMatching products:\n")

        for i, product in enumerate(products, start=1):
            print(
                f"{i}. {product.get('product_name')} "
                f"({product.get('brand')})"
            )

        try:
            choice = int(
                input("\nChoose a product (0 to cancel): ")
            )
        except ValueError:
            print("Invalid selection.")
            return

        if choice == 0:
            return

        if 1 <= choice <= len(products):
            print_product(products[choice - 1])
        else:
            print("Invalid selection.")

    else:
        # Barcode search returns one product
        print_product(result)