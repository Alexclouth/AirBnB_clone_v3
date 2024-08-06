#!/usr/bin/python3
"""
app.py

This module initializes and configures the Flask application for the AirBnB clone API.
It sets up the necessary routes, middleware, and database connections.

Usage:
    Run this module directly to start the Flask application.

Example:
    $ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
      HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 \
      HBNB_API_PORT=5000 python3 -m api.v1.app
"""
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the API
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint for the API views
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """
    Closes the storage on teardown of the app context.

    Args:
        exception (Exception): The exception that triggered the teardown, if any.

    Returns:
        None
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors by returning a JSON response with an error message.

    Args:
        exception (HTTPException): The HTTP exception that triggered the error handler.

    Returns:
        Response: A JSON response with a 404 status code and error message.
    """
    data = {
        "error": "Not found"
    }
    resp = jsonify(data)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    """
    Main entry point for the Flask application.
    Configures the app to run on the specified host and port.
    """
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"), port=int(getenv("HBNB_API_PORT", 5000)))
