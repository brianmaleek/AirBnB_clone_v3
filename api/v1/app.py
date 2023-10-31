#!/usr/bin/python3
"""
module for flask REST App
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


""" Create the flask app """
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_db(exception):
    """ close the storage when the app context is torn down"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 error handler """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ Run the app """
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
