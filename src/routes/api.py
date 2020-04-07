#!/usr/bin/env python3
from flask import jsonify, Blueprint, request
from setup import db
from src.api.users import api_handle_collection_add

routes = Blueprint('api', __name__)


@routes.route('/api/v1/users', methods=['GET'])
def users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    response = []
    users = db.get_users()

    for user in users:
        user.update({"profile": request.host_url + "users/" + user['username']})
        response.append(user)

    return jsonify(response)


@routes.route('/api/v1/users/collection', methods=['GET', 'POST'])
def users_collection():
    """
    Get the games collection of a given user.
    """
    username = request.args.get('username')

    if 'POST' == request.method:
        return jsonify(api_handle_collection_add(username))

    return jsonify(db.get_user_collection(username))


@routes.route('/api/v1/games', methods=['GET'])
def games():
    """
    Get a list of all of the games in the database.

    @TODO Clearly this and other API endpoints will need to be paginated.
    """
    return jsonify(db.get_games())
