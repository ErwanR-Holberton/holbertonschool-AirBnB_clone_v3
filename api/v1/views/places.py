#!/usr/bin/python3
"""view for place"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, abort, request


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """get all places"""
    places = storage.all(Place).values()
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """return json of a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a place using id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """creates a new place"""
    req = request.get_json()

    if req is None:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')

    new_place = Place(name=req['name'])
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200
