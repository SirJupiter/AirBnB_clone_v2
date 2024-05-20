#!/usr/bin/python3
"""This module starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def route():
    """Function displays an HTML page

    Return:
        render_template 7-states_list.html
    """
    def sort_by_name(state):
        """Sorts a state object by its name attribute"""
        return state.name

    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
