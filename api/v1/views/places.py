#!/usr/bin/python3
"""Places search view
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.place import Place
from models.state import State
from models.city import City


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def search_place():
    """get all places"""
    places = storage.all(Place).values()
    req = request.get_json(silent=True)
    if req is None:
        abort(400, description="Not a JSON")
    if len(req) == 0:
        return jsonify(places)

    state_ids = req.get("states", None)
    city_ids = req.get("cities", None)
    amenity_ids = req.get("amenities", None)
    places_in_state = []
    places_in_cities = []

    if isinstance(state_ids, list):
        states = [storage.get(State, id) for id in state_ids]
        cities = [[city for city in state.cities] for state in states if state]
        for city in cities:
            places_in_state.extend([place for place in city.places
                                    if place not in places_in_state])

    if isinstance(city_ids, list):
        cities = [storage.get(City, id) for id in city_ids]
        for city in cities:
            places_in_cities.extend([place for place in city.places
                                    if place not in places_in_cities])

    places_in_cities.extend(places_in_state)
    places_filtered = set(places_in_cities)
    if len(places_filtered) == 0 and not state_ids and not city_ids:
        new_places = []
        for place in places:
            if all(map(lambda amenity_id: 1 if amenity_id in
                       [amenity.id for amenity in place.amenities]
                       else 0, amenity_ids)):
                new_places.append(place)
        return jsonify(new_places)

    if len(amenity_ids) == 0:
        return jsonify(places_filtered)

    new_places = []
    for place in places_filtered:
        if all(map(lambda amenity_id: 1 if amenity_id in
                   [amenity.id for amenity in place.amenities]
                   else 0, amenity_ids)):
            new_places.append(place)
    return jsonify(new_places)
