#!/usr/bin/python3
"""Places_Reviews view
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
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def places_review(place_id=None):
    """ Retrieves all reviews of a place.
        Creates a review for a place.
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.reviews)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")

        if 'user_id' not in req.keys():
            abort(400, "Missing user_id")

        if 'text' not in req.keys():
            abort(400, "Missing text")

        user = storage.get(User, req['user_id'])
        if user is None:
            abort(404)

        review = Review(**req)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id=None):
    """ Retrieves, Deletes or Updates a reviews.
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        req = request.get_json(silent=True)
        if req is None:
            abort(400, "Not a JSON")
        review.update(req)
        return jsonify(review.to_dict())
