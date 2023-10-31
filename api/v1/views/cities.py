#!/usr/bin/python3
"""
This module creates City objects handling all default RestFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response


def custom_make_response(status_code, message=None):
    """ Creates a custom response """
    response = {'error': message}
    return make_response(jsonify(response), status_code)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        return custom_make_response(404, 'State Not found')
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


def get_cities_by_state(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        return None
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return cities_list


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city_id(city_id):
    """ Retrieves a specific City object by Id """
    city = storage.get(City, city_id)
    if city is None:
        return custom_make_response(404, 'City Not found')
    return (jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def city_delete(city_id):
    """ Deletes a City object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return custom_make_response(404, 'City Not found')
    storage.delete(city_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def city_create(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if state is None:
        return custom_make_response(404, 'State Not found')
    city_dict = request.get_json()
    if city_dict is None:
        return custom_make_response(400, 'Not a JSON')
    if 'name' not in city_dict:
        return custom_make_response(400, 'Missing name')
    city_dict['state_id'] = state_id
    new_city = City(**city_dict)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def city_update(city_id):
    """ Updates a City object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return custom_make_response(404, 'City Not found')
    city_dict = request.get_json()
    if city_dict is None:
        return custom_make_response(400, 'Not a JSON')
    for key, value in city_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    city_obj.save()
    return (jsonify(city_obj.to_dict()), 200)
