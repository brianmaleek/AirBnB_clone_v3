#!/usr/bin/python3
"""
This module creates Amenities objects handling all default RestFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


def custom_make_response(status_code, message=None):
    """ Creates a custom response """
    response = {'error': message}
    return make_response(jsonify(response), status_code)


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities_list = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity_id(amenity_id):
    """ Retrieves a specific Amenity object by Id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return custom_make_response(404, 'Amenity Not found')
    return (jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def amenity_delete(amenity_id):
    """ Deletes a Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return custom_make_response(404, 'Amenity Not found')
    storage.delete(amenity_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_create():
    """ Creates a Amenity """
    amenity_dict = request.get_json()
    if amenity_dict is None:
        return custom_make_response(400, 'Not a JSON')
    if 'name' not in amenity_dict:
        return custom_make_response(400, 'Missing name')
    new_amenity = Amenity(**amenity_dict)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def amenity_update(amenity_id):
    """ Updates a Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return custom_make_response(404, 'Amenity Not found')
    amenity_dict = request.get_json()
    if amenity_dict is None:
        return custom_make_response(400, 'Not a JSON')
    for key, value in amenity_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return (jsonify(amenity_obj.to_dict()), 200)
