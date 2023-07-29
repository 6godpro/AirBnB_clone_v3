#!/usr/bin/python3
"""Place View
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=['GET', 'POST'], strict_slashes=False)
def get_or_create_places(city_id=None):
    """Retrieve all place objects of <city_id> or create a place using <city_id>
    methods-allowed: GET -> get all places in in <city_id>
                     POST -> create a place object using <city_id>
    """
    city = storage.get(City, id=city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in city.places])

    if request.method == 'POST':
        req = request.get_json(silent=True)
        user_id = req.get('user_id', None)
        if req is None:
            abort(400, description="Not a JSON")
        if user_id is None:
            abort(400, description="Missing user_id")
        if 'name' not in req.keys():
            abort(400, description="Missing name")

        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        req["city_id"] = city_id
        place = Place(**req)
        place.save()
        return make_response(place.to_dict(), 201)


@app_views.route("/places/<place_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def delete_get_or_update_place(place_id=None):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        req = request.get_json(silent=True)
        if req is None:
            abort(400, description="Not a JSON")
        place.update(req,
                     ignore=["id", "user_id", "city_id", "created_at", "__class__"])
        return jsonify(place.to_dict())
