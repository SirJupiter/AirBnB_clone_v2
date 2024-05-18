#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask, render_template

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


# @app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>', defaults={'text': 'is cool'},
           strict_slashes=False)
def python(text):
    """Function displays a web page with a message

    Return:
        "Python <text>"
    """
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Function displays a web page with a message

    Return:
        "n is a number"
    """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Function displays a web page with a message

    Return:
        render_template rendering 5-number.html
    """
    # if n is int:
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
