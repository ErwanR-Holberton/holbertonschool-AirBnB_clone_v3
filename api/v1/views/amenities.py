#!/usr/bin/python3
from flask import Flask, jsonify, abort, request
from models import Amenity

app = Flask(__name__)

@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict() for amenity in Amenity.all()]
    return jsonify(amenities)

@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return jsonify({}), 200

@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
