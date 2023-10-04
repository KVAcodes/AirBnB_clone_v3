#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the Amenity
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_or_amenities(amenity_id=None):
    """Retrieves a list of all Amenity objects or an Amenity with
    id matching amenity_id.
    """
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        else:
            abort(404)
    else:
        amenities = [amenity.to_dict() for amenity in
                     storage.all(Amenity).values()]
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object with id matching amenity_id.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object.
    """
    if request.is_json:
        amenity_json = request.get_json()
        if 'name' not in amenity_json:
            abort(400, "Missing name")
        else:
            amenity_created = Amenity(**amenity_json)
            amenity_created.save()
            return jsonify(amenity_created.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the attributes of an Amenity Object.
    """
    stored_amenity = storage.get(Amenity, amenity_id)
    if stored_amenity:
        if request.is_json:
            updated_dict = stored_amenity.to_dict()
            keys_to_ignore = ['id', 'created_at', 'updated_at']
            amenity_retrieved = request.get_json()
            for key, val in amenity_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_amenity)
            updated_amenity = Amenity(**updated_dict)
            updated_amenity.save()
            return jsonify(updated_amenity.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
