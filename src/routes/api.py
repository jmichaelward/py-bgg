#!/usr/bin/env python3
from flask import jsonify, Blueprint, request
from app import db
from src.model.user import User, user_schema, users_schema
from src.model.game import Game, game_schema, games_schema
from src.api.users import api_handle_collection_add

routes = Blueprint('api', __name__)


@routes.route('/api/v1/users', methods=['GET'])
def get_users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    users = User.query.all()

    return jsonify(users_schema.dump(users)) if users else jsonify(message="No users found."), 404


@routes.route('/api/v1/users/<username>')
def get_user(username: str):
    """
    Get information about a given user.
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify(message="No user exists for username: " + username), 404

    return jsonify(user_schema.dump(user))


@routes.route('/api/v1/users/<username>/collection', methods=['GET', 'POST'])
def users_collection(username: str):
    """
    Get the games collection of a given user.
    """
    if 'POST' == request.method:
        return jsonify(api_handle_collection_add(username))

    return jsonify(db.get_user_collection(username))


@routes.route('/api/v1/games/<string:title>', methods=['GET'])
def get_game_by_title(title: str):
    game = Game.query.filter_by(title=title).first()

    return jsonify(game_schema.dump(game)) if game else jsonify(message="No game found by title: " + title), 404


@routes.route('/api/v1/games', methods=['GET'])
def get_games():
    """
    Get a list of all of the games in the database.
    """
    games = Game.query.all()

    return jsonify(games_schema.dump(games)) if games else jsonify("No games found."), 404
