#!/usr/bin/python3
"""Amenity view
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'])
def amenities():
    """Retrieve all amenities or creates a new amenity.
    """
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in storage.all(Amenity).values()])

    if request.method == 'POST':
        req = request.get_json(silent=True)
        if req is None:
            abort(400, "Not a JSON")
        if 'name' not in req.keys():
            abort(400, "Missing name")
        amenity = Amenity(**req)
        amenity.save()
        return make_response(amenity.to_dict(), 201)


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'])
def amenities_id(amenity_id=None):
    """Retrieves, updates, or deletes a amenity.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        req = request.get_json(silent=True)
        if req is None:
            abort(400, "Not a JSON")
        amenity.update(req, ignore=["id", "user_id",
                       "place_id", "created_at", "__class__"])
        return jsonify(amenity.to_dict())
