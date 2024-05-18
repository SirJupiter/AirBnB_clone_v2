#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def route():
    """Function displays a web page with a message

    Return:
        "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Function displays a web page with a message

    Return:
        "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Function displays a web page with a message

    Return:
        "C <text>"
    """
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
