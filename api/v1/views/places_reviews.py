#!/usr/bin/python3
""" View that handles all default RESTFul API actions for the Place
object.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves a list of all Review objects linked to a Place
    by place_id
    """
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review Object with id matching review_id.
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review  object with id matching review_id.
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review object for a place with id matching place_id.
    """
    place = storage.get(Place, place_id)
    if place:
        if request.is_json:
            review_json = request.get_json()
            if 'user_id' not in review_json:
                abort(400, "Missing user_id")
            user = storage.get(User, review_json['user_id'])
            if not user:
                abort(404)
            if 'text' not in review_json:
                abort(400, "Missing text")
            review_created = Review(**review_json, place_id=place_id)
            review_created.save()
            return jsonify(review_created.to_dict()), 201
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates the attributes of a Review Object.
    """
    stored_review = storage.get(Review, review_id)
    if stored_review:
        if request.is_json:
            updated_dict = stored_review.to_dict()
            keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at',
                              'updated_at']
            review_retrieved = request.get_json()
            for key, val in review_retrieved.items():
                if key not in keys_to_ignore and key in updated_dict:
                    updated_dict[key] = val
            storage.delete(stored_review)
            updated_review = Review(**updated_dict)
            updated_review.save()
            return jsonify(updated_review.to_dict()), 200
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
