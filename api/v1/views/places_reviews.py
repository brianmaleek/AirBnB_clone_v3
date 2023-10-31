#!/usr/bin/python3
"""
module creates Review objects that handles all default RestFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review
from flask import jsonify, abort, request, make_response


def custom_make_response(status_code, message=None):
    """ Creates a custom response """
    response = {'error': message}
    return make_response(jsonify(response), status_code)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        return custom_make_response(404, 'Place Not found')
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review_by_id(review_id):
    """ Retrieves a specific Review object by Id """
    review = storage.get(Review, review_id)
    if review is None:
        return custom_make_response(404, 'Review Not found')
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def review_delete(review_id):
    """ Deletes a Review object """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        return custom_make_response(404, 'Review Not found')
    storage.delete(review_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def review_create(place_id):
    """ Create a new Review object for a specific Place """
    place = storage.get(Place, place_id)
    if place is None:
        return custom_make_response(404, 'Place Not found')
    review_dict = request.get_json()
    if review_dict is None:
        return custom_make_response(400, 'Not a JSON')
    if 'user_id' not in review_dict:
        return custom_make_response(400, 'Missing user_id')
    if 'text' not in review_dict:
        return custom_make_response(400, 'Missing text')
    user = storage.get(User, review_dict['user_id'])
    if user is None:
        return custom_make_response(404, 'User Not found')
    review_dict['place_id'] = place_id
    new_review = Review(**review_dict)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def review_update(review_id):
    """ Updates a Review object """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        return custom_make_response(404, 'Review Not found')
    review_dict = request.get_json()
    if review_dict is None:
        return custom_make_response(400, 'Not a JSON')
    for key, value in review_dict.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review_obj, key, value)
    review_obj.save()
    return (jsonify(review_obj.to_dict()), 200)
