# OpenFoodFacts integration
"""
OpenFoodFacts Service

Handles all communication with the
OpenFoodFacts API.
"""

import requests  # type: ignore[import-not-found]

from config import Config

from utils.logger import logger


class OpenFoodFactsService:

    BASE_URL = Config.OPENFOODFACTS_URL

    TIMEOUT = Config.REQUEST_TIMEOUT

    #########################################################
    # PRIVATE HELPERS
    #########################################################

    @staticmethod
    def _normalize_product(product):
        """
        Normalize product fields returned
        by OpenFoodFacts.
        """

        return {

            "barcode":
                product.get("code", ""),

            "product_name":
                product.get("product_name", ""),

            "brand":
                product.get("brands", ""),

            "ingredients":
                product.get(
                    "ingredients_text",
                    ""
                ),

            "categories":
                product.get(
                    "categories",
                    ""
                ),

            "quantity":
                product.get(
                    "quantity",
                    ""
                ),

            "image":
                product.get(
                    "image_url",
                    ""
                ),

            "nutriscore":
                product.get(
                    "nutriscore_grade",
                    ""
                )

        }

    #########################################################
    # SEARCH BY BARCODE
    #########################################################

    @classmethod
    def search_by_barcode(
        cls,
        barcode
    ):
        """
        Search OpenFoodFacts by barcode.
        """

        url = (
            f"{cls.BASE_URL}"
            f"/api/v0/product/"
            f"{barcode}.json"
        )

        try:

            response = requests.get(
                url,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            if data.get("status") == 0:

                logger.warning(
                    f"Barcode not found: "
                    f"{barcode}"
                )

                return None

            product = data.get(
                "product",
                {}
            )

            logger.info(
                f"Barcode lookup: "
                f"{barcode}"
            )

            return cls._normalize_product(
                product
            )

        #####################################################
        # API ERRORS
        #####################################################

        except requests.Timeout:

            logger.error(
                "OpenFoodFacts timeout"
            )

            return {
                "error":
                    "Request timed out"
            }

        except requests.ConnectionError:

            logger.error(
                "Connection error"
            )

            return {
                "error":
                    "Unable to connect "
                    "to OpenFoodFacts"
            }

        except requests.HTTPError as exc:

            logger.error(str(exc))

            return {
                "error":
                    "Unexpected API response"
            }

        except Exception as exc:

            logger.exception(exc)

            return {
                "error":
                    str(exc)
            }

    #########################################################
    # SEARCH BY PRODUCT NAME
    #########################################################

    @classmethod
    def search_by_name(
        cls,
        product_name
    ):
        """
        Search OpenFoodFacts by name.
        """

        url = (
            f"{cls.BASE_URL}"
            "/cgi/search.pl"
        )

        params = {

            "search_terms":
                product_name,

            "search_simple":
                1,

            "action":
                "process",

            "json":
                1

        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            products = []

            for product in data.get(
                "products",
                []
            ):

                products.append(
                    cls._normalize_product(
                        product
                    )
                )

            logger.info(
                f"Product search: "
                f"{product_name}"
            )

            return products

        except requests.Timeout:

            logger.error(
                "Search timeout"
            )

            return []

        except requests.ConnectionError:

            logger.error(
                "Connection error"
            )

            return []

        except Exception as exc:

            logger.exception(exc)

            return []

    #########################################################
    # INVENTORY FORMAT
    #########################################################

    @staticmethod
    def to_inventory_product(
        product
    ):
        """
        Convert OpenFoodFacts product
        into inventory format.
        """

        if not product:
            return None

        return {

            "barcode":
                product.get(
                    "barcode",
                    ""
                ),

            "product_name":
                product.get(
                    "product_name",
                    ""
                ),

            "brand":
                product.get(
                    "brand",
                    ""
                ),

            "ingredients":
                product.get(
                    "ingredients",
                    ""
                ),

            #################################################
            # These do not exist in OpenFoodFacts
            #################################################

            "price": 0,

            "stock": 0

        }