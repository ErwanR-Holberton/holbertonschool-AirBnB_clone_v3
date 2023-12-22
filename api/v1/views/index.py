#!/usr/bin/python3
"""defines endpoints and their output """
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """the client gets the status if the server is reachable and working"""
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats)
