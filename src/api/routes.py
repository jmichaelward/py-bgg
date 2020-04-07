#!/usr/bin/env python3
from flask import jsonify, Blueprint
from src.db import Database

api = Blueprint('api', __name__)

# @TODO Figure out how to make a shared database instance.
db = Database()
db.connect()


@api.route('/api/v1/users', methods=['GET'])
def users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    return jsonify(db.get_users())


@api.route('/api/v1/games', methods=['GET'])
def games():
    """
    Get a list of all of the games in the database.

    @TODO Clearly this and other API endpoints will need to be paginated.
    """
    return jsonify(db.get_games())
