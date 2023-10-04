#!/usr/bin/python3
""" index """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})
