#!/usr/bin/python3
"""This module imports app from __init__.py
app is an instance of the Flask object with "__name__ passed to it
"""

from web_flask import app


if __name__ == "__main__":
    """Main function that runs the app"""
    app.run(debug=True, host="0.0.0.0", port=5000)
