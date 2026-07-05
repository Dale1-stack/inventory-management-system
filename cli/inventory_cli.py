#!/usr/bin/env python3
"""
Inventory Management CLI
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .menu import (
        main_menu,
        view_all_items,
        search_item,
        add_item,
        update_item,
        delete_item,
        fetch_product,
        import_product,
        enriched_item,
    )
except ImportError:
    from cli.menu import (
        main_menu,
        view_all_items,
        search_item,
        add_item,
        update_item,
        delete_item,
        fetch_product,
        import_product,
        enriched_item,
    )


def run():
    actions = {
        "1": view_all_items,
        "2": search_item,
        "3": add_item,
        "4": update_item,
        "5": delete_item,
        "6": fetch_product,
        "7": import_product,
        "8": enriched_item,
    }

    while True:
        choice = main_menu()

        if choice == "0":
            print("\nGoodbye!\n")
            break

        action = actions.get(choice)

        if action is None:
            print("\nInvalid option.")
            continue

        try:
            action()
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    run()