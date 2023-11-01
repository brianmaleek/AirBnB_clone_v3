#!/usr/bin/python3
""" contains the index view for the API """

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def get_status():
    """ returns a JSON status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def get_stats():
    """ retrieves the number of each objects by type """
    stats = {
        "states": storage.count(State),
        "cities": storage.count(City),
        "amenities": storage.count(Amenity),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "users": storage.count(User)
    }
    return jsonify(stats)
