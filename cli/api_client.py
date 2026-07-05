"""
HTTP client used by the Inventory Management CLI.

Provides a thin wrapper around the Flask REST API and the
OpenFoodFacts integration endpoint.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

DEFAULT_BASE_URL = "http://127.0.0.1:5000"

TIMEOUT = 10


class APIClientError(Exception):
    """Raised when an API request fails."""


class APIClient:
    """Simple REST client for the Inventory API."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=TIMEOUT,
                **kwargs,
            )

            response.raise_for_status()

            if response.status_code == 204:
                return None

            if response.content:

                payload = response.json()

                if not payload.get("success", True):
                    raise APIClientError(
                        payload.get("message", "API request failed")
                    )
                
                return payload.get("data")
            
            return None
        
        except requests.exceptions.HTTPError as exc:
            try:
                message = response.json().get("message", response.text)
            except Exception:
                message = response.text

            raise APIClientError(
                f"{response.status_code}: {message}"
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            raise APIClientError(
                "Could not connect to the Inventory API."
            ) from exc

        except requests.exceptions.Timeout as exc:
            raise APIClientError(
                "The request timed out."
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise APIClientError(str(exc)) from exc

    # ---------- Inventory ----------

    def get_items(self) -> List[Dict]:
        return self._request("GET", "/inventory")

    def get_item(self, item_id: int) -> Optional[Dict]:
        return self._request("GET", f"/inventory/{item_id}")

    def create_item(self, payload):
        return self._request(
            "POST",
            "/inventory",
            json=payload,
        )

    def update_item(
        self,
        item_id,
        payload
    ):
        return self._request(
            "PUT",
            f"/inventory/{item_id}",
            json=payload,
        )

    def delete_item(self, item_id):
        self._request(
            "DELETE",
            f"/inventory/{item_id}",
        )
        return True

    # ---------- OpenFoodFacts ----------

    def fetch_openfoodfacts(self, query):
        if query.isdigit():
            endpoint = f"/inventory/search/barcode/{query}"
        else:
            endpoint = f"/inventory/search/name/{query}"
        return self._request(
              "GET",
endpoint
    )


_client = APIClient()


def get_items() -> List[Dict]:
    return _client.get_items()


def get_item(item_id: int) -> Optional[Dict]:
    return _client.get_item(item_id)


def create_item(payload: Dict) -> Dict:
    return _client.create_item(payload)


def update_item_api(
    item_id: int,
    payload: Dict,
) -> Dict:
    return _client.update_item(item_id, payload)


def delete_item_api(item_id: int) -> bool:
    return _client.delete_item(item_id)


def fetch_openfoodfacts(query: str) -> Optional[Dict]:
    return _client.fetch_openfoodfacts(query)