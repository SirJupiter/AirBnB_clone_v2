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
