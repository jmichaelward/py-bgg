#!/usr/bin/env python3
from app import app, db
from flask import jsonify
from flask.views import MethodView
from src.bgg_api import BggApi
from src.model.user import User, user_schema, user_game_collection, games_collection_schema
from src.model.game import Game, games_schema
from flask_smorest import Blueprint
from sqlalchemy import and_

api = Blueprint('users_collection_api', 'users_collection_api',
                url_prefix='/api/v1/collection', description='Users Collection API')


def register_routes():
    app.register_blueprint(api)


@api.route('/<string:username>', methods=['GET', 'POST'])
class UserGamesCollection(MethodView):
    def get(self, username: str):
        """
        Get the games collection of a given user.
        """
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify(message="No user exists by username " + username), 404

        collection = get_collection(user)

        return jsonify(user=user_schema.dump(user), collection=games_schema.dump(collection))

    def post(self, username: str):
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify(message="No user exists by username " + username), 404

        collection = update_collection(user)

        return jsonify(user=user_schema.dump(user), collection=games_collection_schema.dump(collection))


def add_to_collection(user: User, game: Game):
    if not user and game:
        return jsonify(message="Could not find both user and game"), 404

    if user_has_game(user, game):
        return jsonify(message="User " + user.username + " already has game " + game.title + " in collection."), 200

    if add_game_to_user_collection(user, game):
        return jsonify(message="successfully added " + game.title + " to collection for " + user.username), 200

    return jsonify(message="Failed to add user for some unknown reason."), 503


def user_has_game(user: User, game: Game):
    return db.session.execute(
        user_game_collection.select().where(
            and_(
                user_game_collection.c.user_id == user.id,
                user_game_collection.c.game_id == game.id
            )
        )
    ).fetchone()


def add_game_to_user_collection(user: User, game: Game):
    result = db.session.execute(
        user_game_collection.insert(), {"user_id": user.id, "game_id": game.id}
    )

    db.session.commit()

    return result


def update_collection(user: User):
    response, userdata = BggApi().get_json('collection?username=' + user.username)

    if 200 != response.status_code:
        return get_collection_response(response)

    games = userdata['items']['item'] if "item" in userdata['items'] else []

    if 0 == len(games):
        return []

    for game in games:
        new_game = create_game(Game(bgg_id=game['@objectid'], title=game['name']['#text']))
        add_to_collection(user, new_game)

    return get_collection(user)


def get_collection(user: User):
    return Game.query.join(
        user_game_collection
    ).filter(user_game_collection.c.user_id == user.id).all()


def get_collection_response(response):
    """
    Get an appropriate response for a non-200 response to the /collections endpoint.
    :param response:
    :return:
    """
    if 202 == response.status_code:
        return []  # @TODO Figure out how to handle BGG's response that it's processing user data.
    elif 404 == response.status_code:
        return []  # @TODO Figure out whether this is actually a code BGG returns and what to do in this case.

    return []  # @TODO Figure out whether there are other responses to handle. There certainly are.


def create_game(game: Game):
    """
    Insert a game into the database.
    """
    existing_game = Game.query.filter_by(bgg_id=game.bgg_id).first()

    if existing_game:
        return existing_game

    db.session.add(game)
    db.session.commit()

    return game
