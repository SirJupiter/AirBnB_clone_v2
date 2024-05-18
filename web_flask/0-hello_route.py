#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def route():
    """Function displays a web page eith a message

    Return:
        "Hello HBNB!"
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    """Main function that runs the app"""
    app.run(debug=True, host="0.0.0.0", port=5000)
