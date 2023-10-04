#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the User
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_or_users(user_id=None):
    """Retrieves a list of all User objects or an User object with
    id matching user_id.
    """
    if user_id:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            abort(404)
    else:
        users = [user.to_dict() for user in
                 storage.all(User).values()]
        return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes an User object with id matching user_id.
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates an User object.
    """
    if request.is_json:
        user_json = request.get_json()
        if 'email' not in user_json:
            abort(400, "Missing email")
        if 'password' not in user_json:
            abort(400, "Missing password")
        user_created = User(**user_json)
        user_created.save()
        return jsonify(user_created.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates the attributes of an User Object.
    """
    stored_user = storage.get(User, user_id)
    if stored_user:
        if request.is_json:
            updated_dict = stored_user.to_dict()
            keys_to_ignore = ['id', 'email', 'created_at', 'updated_at']
            user_retrieved = request.get_json()
            for key, val in user_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_user)
            updated_user = User(**updated_dict)
            updated_user.save()
            return jsonify(updated_user.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
