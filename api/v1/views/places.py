#!/usr/bin/python3
"""
This module creates Places objects handling all default RestFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response


def custom_make_response(status_code, message=None):
    """ Creates a custom response """
    response = {'error': message}
    return make_response(jsonify(response), status_code)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places_by_city(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        return custom_make_response(404, 'City Not found')
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place_by_id(place_id):
    """ Retrieves a specific Place object by Id """
    place = storage.get(Place, place_id)
    if place is None:
        return custom_make_response(404, 'Place Not found')
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """ Deletes a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return custom_make_response(404, 'Place Not found')
    storage.delete(place_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def place_create(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        return custom_make_response(404, 'City Not found')
    place_dict = request.get_json()
    if place_dict is None:
        return custom_make_response(400, 'Not a JSON')
    if 'user_id' not in place_dict:
        return custom_make_response(400, 'Missing user_id')
    user = storage.get(User, place_dict['user_id'])
    if user is None:
        return custom_make_response(404, 'User Not found')
    if 'name' not in place_dict:
        return custom_make_response(400, 'Missing name')
    place_dict['city_id'] = city_id
    new_place = Place(**place_dict)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """ Updates a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return custom_make_response(404, 'Place Not found')
    place_dict = request.get_json()
    if place_dict is None:
        return custom_make_response(400, 'Not a JSON')
    for key, value in place_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    place_obj.save()
    return (jsonify(place_obj.to_dict()), 200)
