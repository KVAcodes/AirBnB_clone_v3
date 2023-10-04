#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the City
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves a list of all City objects linked to a State
    by state_id
    """
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City Object with id matching city_id.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object with id matching city_id.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a city object for a state with id matching state_id.
    """
    state = storage.get(State, state_id)
    if state:
        if request.is_json:
            city_json = request.get_json()
            if 'name' not in city_json:
                abort(400, "Missing name")
            else:
                city_created = City(**city_json, state_id=state_id)
                city_created.save()
                return jsonify(city_created.to_dict()), 201
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates the attributes of a City Object.
    """
    stored_city = storage.get(City, city_id)
    if stored_city:
        if request.is_json:
            updated_dict = stored_city.to_dict()
            keys_to_ignore = ['id', 'state_id', 'created_at', 'updated_at']
            city_retrieved = request.get_json()
            for key, val in city_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_city)
            updated_city = City(**updated_dict)
            updated_city.save()
            return jsonify(updated_city.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
