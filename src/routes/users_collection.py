#!/usr/bin/env python3
from app import app, db
from flask import jsonify
from flask.views import MethodView
from src.bgg_api import BggApi
from src.model.user import User, user_schema, user_game_collection, games_collection_schema
from src.model.game import Game, games_schema
from flask_smorest import Blueprint

api = Blueprint('users_collection_api', 'users_collection_api',
                url_prefix='/api/v1/collection', description='Users Collection API')


def register_routes():
    app.register_blueprint(api)


@api.route('/<string:username>/', methods=['GET', 'POST'])
class UserGamesCollection(MethodView):
    def get(self, username: str):
        """
        Get the games collection of a given user.
        """
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify(message="No user exists by username " + username), 404

        return jsonify(user=user_schema.dump(user), collection=games_schema.dump(user.get_collection()))

    def post(self, username: str):
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify(message="No user exists by username " + username), 404

        return jsonify(user=user_schema.dump(user), collection=games_schema.dump(self.update(user)))

    def update(self, user: User):
        response, userdata = BggApi().get_json('collection?username=' + user.username)

        if 200 != response.status_code:
            return []

        games = userdata['items']['item'] if "item" in userdata['items'] else []

        if 0 == len(games):
            return []

        for game in games:
            new_game = Game(bgg_id=game['@objectid'], title=game['name']['#text'])
            new_game.create_record()
            user.add_game_to_collection(new_game)

        return user.get_collection()
