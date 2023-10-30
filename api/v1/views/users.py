#!/usr/bin/python3
"""
This module creates User object that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response


def custom_make_response(status_code, message=None):
    """ Creates a custom response """
    response = {'error': message}
    return make_response(jsonify(response), status_code)


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_id(user_id):
    """ Retrieves a specific User object by Id """
    user = storage.get(User, user_id)
    if user is None:
        return custom_make_response(404, 'User Not found')
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def user_delete(user_id):
    """ Deletes a User object """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return custom_make_response(404, 'User Not found')
    storage.delete(user_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_create():
    """ Creates a User """
    user_dict = request.get_json()
    if user_dict is None:
        return custom_make_response(400, 'Not a JSON')
    if 'email' not in user_dict:
        return custom_make_response(400, 'Missing email')
    if 'password' not in user_dict:
        return custom_make_response(400, 'Missing password')
    new_user = User(**user_dict)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def user_update(user_id):
    """ Updates a User object """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return custom_make_response(404, 'User Not found')
    user_dict = request.get_json()
    if user_dict is None:
        return custom_make_response(400, 'Not a JSON')
    for key, value in user_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    user_obj.save()
    return (jsonify(user_obj.to_dict()), 200)
