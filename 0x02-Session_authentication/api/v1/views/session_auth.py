#!/usr/bin/env python3
"""session_auth.py"""
import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """
    POST /api/v1/auth_session/login
    Return:User instance JSON represented """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if user is None or user == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            cookie_name = os.getenv('SESSION_NAME')
            response.set_cookie(cookie_name, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """ DELETE /api/v1/auth_session/logout"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    else:
        return jsonify({}), 200
