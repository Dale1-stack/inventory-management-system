"""
Inventory Management System

Application Entry Point
"""

from flask import Flask  # type: ignore[import]

from config import Config

from routes.inventory_routes import inventory_bp

from utils.logger import configure_logging


def create_app():

    app = Flask(__name__)

    ####################################################
    # Configuration
    ####################################################

    app.config.from_object(Config)

    ####################################################
    # Logging
    ####################################################

    configure_logging()

    ####################################################
    # Register Blueprints
    ####################################################

    app.register_blueprint(inventory_bp)

    ####################################################
    # Error Handlers
    ####################################################

    @app.errorhandler(404)
    def not_found(error):

        return {

            "success": False,

            "message": "Endpoint not found"

        }, 404

    @app.errorhandler(405)
    def method_not_allowed(error):

        return {

            "success": False,

            "message": "Method not allowed"

        }, 405

    @app.errorhandler(500)
    def internal(error):

        return {

            "success": False,

            "message": "Internal Server Error"

        }, 500

    ####################################################
    # Home Route
    ####################################################

    @app.route("/")

    def home():

        return {

            "application":
                "Inventory Management API",

            "version":
                "1.0",

            "status":
                "running"

        }

    return app


###########################################################

app = create_app()

###########################################################

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
