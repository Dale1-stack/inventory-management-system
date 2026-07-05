#!/usr/bin/env python3
"""
Inventory Management CLI

Entry point for interacting with the Inventory Management REST API.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .menu import (
        add_item,
        update_item,
        delete_item,
        view_all_items,
        search_item,
        fetch_product,
        main_menu,
    )
except ImportError:  # pragma: no cover - fallback for direct script execution
    from cli.menu import (
        add_item,
        update_item,
        delete_item,
        view_all_items,
        search_item,
        fetch_product,
        main_menu,
    )


def run():
    """Run the CLI application."""

    actions = {
        "1": view_all_items,
        "2": search_item,
        "3": add_item,
        "4": update_item,
        "5": delete_item,
        "6": fetch_product,
    }

    while True:
        choice = main_menu()

        if choice == "0":
            print("\nGoodbye!\n")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
            except Exception as exc:
                print(f"\nError: {exc}")
        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    run()