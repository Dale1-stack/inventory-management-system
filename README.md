Inventory Management System

A production-style Inventory Management System built with Flask, featuring a RESTful API, OpenFoodFacts integration, a Command Line Interface (CLI), and comprehensive unit testing.

The system enables employees to manage inventory items through CRUD operations while enriching product information using the OpenFoodFacts API.

Table of Contents
Project Overview
Features
Technologies Used
Project Structure
Installation
Configuration
Running the Application
REST API Endpoints
OpenFoodFacts Integration
CLI Application
Testing
Sample API Requests
Error Handling
Logging
Future Improvements
Troubleshooting
Author
License
Project Overview

This Inventory Management System simulates the administrator portal of an e-commerce platform.

It allows employees to:

View inventory
Add inventory items
Update inventory
Delete inventory items
Search OpenFoodFacts by barcode
Search OpenFoodFacts by product name
Import products directly into inventory
View enriched inventory data combining local inventory with OpenFoodFacts information

The project demonstrates:

Flask REST APIs
External API integration
CRUD operations
Request validation
Pagination
Filtering
Logging
CLI development
Unit testing with pytest
Mocking external APIs
Features
Inventory Management
View all inventory items
View a single inventory item
Add inventory items
Update inventory
Delete inventory items
OpenFoodFacts Integration

Search products by:

Barcode
Product name

Import products directly into local inventory.

Automatically normalize product information.

Filtering

Inventory supports filtering by:

Brand
Product name
Minimum price
Maximum price

Example:

GET /inventory?brand=Silk
Pagination

Supports:

GET /inventory?page=1&limit=10

Returns:

current page
total pages
total records
items
Validation

Incoming requests are validated before processing.

Examples:

Missing required fields
Invalid price
Invalid stock
Duplicate barcode
Logging

Application events are logged including:

API requests
Product imports
Validation failures
Errors
Consistent JSON Responses

Success

{
    "success": true,
    "message": "...",
    "data": {}
}

Error

{
    "success": false,
    "message": "..."
}
Technologies Used

Backend

Python 3
Flask
Requests

CLI

Python

Testing

pytest
unittest.mock

Utilities

Logging
JSON
REST API

External API

OpenFoodFacts
Project Structure
inventory-management-system/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   └── inventory.py
│
├── routes/
│   ├── __init__.py
│   └── inventory_routes.py
│
├── services/
│   ├── __init__.py
│   ├── inventory_service.py
│   └── openfoodfacts.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── responses.py
│   └── validators.py
│
├── cli/
│   ├── inventory_cli.py
│   ├── menu.py
│   ├── api_client.py
│   └── display.py
│
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_inventory_service.py
│   ├── test_openfoodfacts.py
│   └── test_validators.py
│
└── logs/
Installation

Clone the repository

git clone https://github.com/YOUR_USERNAME/inventory-management-system.git

Move into the project

cd inventory-management-system
Create a Virtual Environment

Linux / macOS

python3 -m venv venv

Activate

source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Requirements

Example requirements.txt

Flask
requests
pytest
python-dotenv
click
Configuration

Edit config.py

Example

OPENFOODFACTS_URL = "https://world.openfoodfacts.org"

REQUEST_TIMEOUT = 10

ITEMS_PER_PAGE = 10
Running the Application

Start Flask

python3 app.py

Server

Running on:

http://127.0.0.1:5000
Running the CLI

Open another terminal

python3 cli/inventory_cli.py

Example menu

==========================================
Inventory Management System
==========================================

1. View inventory
2. View one item
3. Add item
4. Update item
5. Delete item
6. Search OpenFoodFacts
0. Exit
REST API Endpoints
Get all inventory
GET /inventory

Supports

?page=
&limit=
&brand=
&product_name=
&min_price=
&max_price=
Get inventory item
GET /inventory/<id>
Create item
POST /inventory

Example

{
    "barcode":"737628064502",
    "product_name":"Organic Almond Milk",
    "brand":"Silk",
    "ingredients":"Filtered water...",
    "price":350,
    "stock":20
}
Update item
PATCH /inventory/<id>

Example

{
    "price":450,
    "stock":50
}
Delete item
DELETE /inventory/<id>
Search barcode
GET /inventory/search/barcode/<barcode>
Search product name
GET /inventory/search/name/<product_name>
Import product
POST /inventory/import/<barcode>

Imports a product directly from OpenFoodFacts into local inventory.

Enriched inventory
GET /inventory/enriched/<id>

Returns local inventory combined with live OpenFoodFacts data.

OpenFoodFacts Integration

The application communicates with the OpenFoodFacts REST API.

Search by barcode

/api/v0/product/<barcode>.json

Search by name

/cgi/search.pl

Returned products are normalized into a consistent internal format.

Example

{
    "barcode":"737628064502",
    "product_name":"Organic Almond Milk",
    "brand":"Silk",
    "ingredients":"Filtered water...",
    "quantity":"946ml",
    "categories":"Plant Based Foods",
    "image":"...",
    "nutriscore":"b"
}
CLI Features

The CLI allows users to:

View inventory
Search inventory by ID
Add products
Update products
Delete products
Search OpenFoodFacts

The CLI communicates with the Flask API using HTTP requests.

Testing

Run all tests

python3 -m pytest

Verbose

python3 -m pytest -v

Run a single test

pytest tests/test_routes.py

Tests include:

CRUD endpoints
Validation
Pagination
Filtering
Inventory service
OpenFoodFacts service
Response helpers
Mocked API requests
Logging

Application logs are written to the logs directory.

Logged events include:

Requests
Imports
Validation failures
API failures
Unexpected exceptions
Error Handling

Common HTTP responses

Code	Description
200	Success
201	Created
400	Bad Request
404	Not Found
405	Method Not Allowed
409	Conflict
500	Internal Server Error

Example

{
    "success": false,
    "message": "Inventory item not found."
}
Example Workflow
Start the Flask server.
python app.py
Start the CLI.
python cli/inventory_cli.py
Add an inventory item.
View the inventory.
Search OpenFoodFacts for a product.
Import a product into inventory.
Update stock or price.
Delete a product.
Future Improvements

Potential enhancements include:

Persistent database integration (PostgreSQL or MySQL)
User authentication and authorization
JWT-based API security
Swagger/OpenAPI documentation
Docker containerization
CI/CD pipeline with GitHub Actions
Inventory export to CSV or Excel
Product image uploads
Barcode scanning support
Role-based access control
Inventory analytics dashboard
Low-stock alerts
Bulk import/export functionality
Troubleshooting
ModuleNotFoundError

Activate your virtual environment and install dependencies:

pip install -r requirements.txt
404 Endpoint not found

Ensure:

The Flask server is running.
The CLI points to http://127.0.0.1:5000.
Routes are registered using:
app.register_blueprint(inventory_bp)
ConnectionError

Verify the Flask server is running before launching the CLI.

OpenFoodFacts requests fail

Check:

Internet connectivity
The configured OpenFoodFacts base URL
API availability
Learning Outcomes

This project demonstrates proficiency in:

Designing RESTful APIs with Flask
Structuring a modular Python application
Consuming and normalizing third-party APIs
Implementing CRUD operations
Applying input validation and error handling
Building a command-line client for an HTTP API
Writing automated tests with pytest and mocks
Using logging for observability
Organizing a maintainable Python codebase
Author

Dale Mukabane

GitHub: https://github.com/YOUR_USERNAME

License

This project is licensed under the MIT License. You are free to use, modify, and distribute it with appropriate attribution.