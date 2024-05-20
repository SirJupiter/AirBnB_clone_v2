#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def route():
    """Displays states and cities listed in alphabetical order

    Return:
        render_template 8-cities_by_states.html
    """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
