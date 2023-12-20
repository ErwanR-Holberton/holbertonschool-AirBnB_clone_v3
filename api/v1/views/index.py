#!/usr/bin/python3
"""defines endpoints and their output """
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/api/v1/stats', strict_slashes=False)
def get_stats():
    """the client gets the status if the server is reachable and working"""
    stats = {}
    types_to_count = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    for obj_type in types_to_count:
        count = storage.count(obj_type)
        stats[obj_type] = count
    return stats
