#!/usr/bin/python3
"""
State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request
import json


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def get_state_id(state_id):
    """ Retrieves a specific State object by Id """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def state_delete(state_id):
    """ Deletes a State object """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def state_create():
    """ Creates a State """
    state_dict = request.get_json()
    if not state_dict:
        abort(400, 'Not a JSON')
    if 'name' not in state_dict:
        abort(400, 'Missing name')
    new_state = State(**state_dict)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def state_update(state_id):
    """ Updates a State object """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    state_dict = request.get_json()
    if not state_dict:
        abort(400, 'Not a JSON')
    for key, value in state_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    state_obj.save()
    return (jsonify(state_obj.to_dict()), 200)
