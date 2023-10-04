#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the State
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state_or_states(state_id=None):
    """Retrieves a list of all State objects or a State with
    id matching state_id.
    """
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    else:
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object with id matching state_id.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object.
    """
    if request.is_json:
        state_json = request.get_json()
        if 'name' not in state_json:
            abort(400, "Missing name")
        else:
            state_created = State(**state_json)
            state_created.save()
            return jsonify(state_created.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates the attributes of a State Object.
    """
    stored_state = storage.get(State, state_id)
    if stored_state:
        if request.is_json:
            updated_dict = stored_state.to_dict()
            keys_to_ignore = ['id', 'created_at', 'updated_at']
            state_retrieved = request.get_json()
            for key, val in state_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_state)
            updated_state = State(**updated_dict)
            updated_state.save()
            return jsonify(updated_state.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
