#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the Place
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves a list of all Place objects linked to a City
    by city_id
    """
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Placr Object with id matching place_id.
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/place/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object with id matching place_id.
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object for a city with id matching city_id.
    """
    city = storage.get(City, city_id)
    if city:
        if request.is_json:
            place_json = request.get_json()
            if 'user_id' not in place_json:
                abort(400, "Missing user_id")
            user = storage.get(User, place_json['user_id'])
            if not user:
                abort(404)
            if 'name' not in place_json:
                abort(404, "Missing Name")
            place_created = Place(**place_json, city_id=city_id,
                                  user_id=user.id)
            place_created.save()
            return jsonify(place_created.to_dict()), 201
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates the attributes of a Place Object.
    """
    stored_place = storage.get(Place, place_id)
    if stored_place:
        if request.is_json:
            updated_dict = stored_place.to_dict()
            keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at',
                              'updated_at']
            place_retrieved = request.get_json()
            for key, val in place_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_place)
            updated_place = Place(**updated_dict)
            updated_place.save()
            return jsonify(updated_place.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
