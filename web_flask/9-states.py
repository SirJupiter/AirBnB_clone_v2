#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def route(state_id=None):
    """Displays states and cities listed in alphabetical order

    Return:
        render_template 9-states.html
    """
    states = storage.all(State)

    if state_id is not None:
        state_id = f"State.{state_id}"

    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
