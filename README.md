# Inventory Management System

A lightweight inventory management application built with Flask, featuring a REST API, an interactive CLI, OpenFoodFacts integration, and automated tests.

## Overview

This project demonstrates a modular Python backend for managing inventory items. It supports:

- CRUD operations for inventory items
- Filtering and pagination
- Validation and consistent JSON responses
- OpenFoodFacts lookup by barcode or product name
- A command-line interface for interacting with the API
- Automated tests with pytest

## Features

### API
- List inventory items with filters and pagination
- Retrieve a single item
- Create, update, and delete items
- Prevent duplicate barcodes
- Return structured success/error responses

### OpenFoodFacts Integration
- Search by barcode
- Search by product name
- Normalize product metadata for local use

### CLI
- Browse inventory from the terminal
- Add, update, and delete items
- Search external product data

## Tech Stack

- Python 3
- Flask
- Requests
- python-dotenv
- pytest
- Click

## Project Structure

```text
inventory-management-system/
+-- app.py
+-- config.py
+-- requirements.txt
+-- README.md
+-- cli/
�   +-- api_client.py
�   +-- display.py
�   +-- inventory_cli.py
�   +-- menu.py
+-- database/
�   +-- inventory.py
+-- routes/
�   +-- inventory_routes.py
+-- services/
�   +-- inventory_service.py
�   +-- openfoodfacts.py
+-- tests/
�   +-- ...
+-- utils/
�   +-- logger.py
�   +-- responses.py
�   +-- validators.py
+-- logs/
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd inventory-management-system
```

2. Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The app uses values from [config.py](config.py) and environment variables where applicable. The default configuration includes:

- Flask secret key
- Debug setting
- OpenFoodFacts API URL
- Request timeout
- Logging location

## Running the Application

### Start the Flask API

```bash
python3 app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

### Start the CLI

```bash
python3 cli/inventory_cli.py
```

## API Endpoints

### Inventory

- GET /inventory
- GET /inventory/<id>
- POST /inventory
- PATCH /inventory/<id>
- DELETE /inventory/<id>

### OpenFoodFacts

- GET /inventory/search/barcode/<barcode>
- GET /inventory/search/name/<product_name>
- POST /inventory/import/<barcode>

## Example Requests

### List inventory

```bash
curl http://127.0.0.1:5000/inventory
```

### Create an inventory item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "barcode": "1234567890123",
    "product_name": "Example Product",
    "brand": "Example Brand",
    "ingredients": "Water",
    "price": 12.5,
    "stock": 10
  }'
```

## Testing

Run the test suite with:

```bash
pytest
```

Or for verbose output:

```bash
pytest -v
```

## Troubleshooting

### ModuleNotFoundError

If imports fail, activate the virtual environment and reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Flask app does not start

Make sure:
- the correct Python environment is active
- dependencies are installed
- the project root is being used when launching the app

## License

This project is licensed under the MIT License.