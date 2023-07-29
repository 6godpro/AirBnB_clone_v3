#!/usr/bin/python3
"""User view
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'])
def users():
    """Retrieves and creates users."""
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in storage.all(User).values()])

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        if 'email' not in req.keys():
            abort(400, "Missing email")
        if 'password' not in req.keys():
            abort(400, "Missing password")
        user = User(**req)
        user.save()
        return make_response(user.to_dict(), 201)


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def users_id(user_id=None):
    """Retrieves, deletes, or updates a user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        user.update(req, ignore=["id",
                    "created_at", "email", "__class__"])
        return jsonify(user.to_dict())
