#!/usr/bin/python3
"""City views"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    if 'name' not in req or not isinstance(req['name'],
                                           str) or not req['name'].strip():
        abort(400, 'Missing name')

    new_city = City(name=req['name'], state_id=state_id)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')

    for key, value in req.items():
        if key == 'name' and (not isinstance(value, str) or not value.strip()):
            abort(400, 'Missing name')
        elif key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
