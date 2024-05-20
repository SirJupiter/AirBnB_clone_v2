#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """Loads State, City and Amenity objects listed in alphabetical order

    Return:
        render_template 6-index.html
    """
    states = storage.all(State).values()
    amenities = storage.all(State).values()

    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
