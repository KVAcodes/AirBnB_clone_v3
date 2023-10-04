#!/usr/bin/python3
"""The api of the HBNB project using flask.
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 not_found errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=host if host else '0.0.0.0',
            port=port if port else 5000,
            threaded=True)
