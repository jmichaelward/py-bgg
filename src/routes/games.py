#!/usr/bin/env python3
from app import app
from flask import jsonify, render_template
from flask.views import MethodView
from flask_smorest import Blueprint
from src.model.game import Game, game_schema, games_schema

api = Blueprint('games_api', 'games_api', url_prefix='/api/v1/games', description="Games API")
view = Blueprint('games_view', 'games_view', url_prefix='/games', description='Operations on games',
                        template_folder='templates')


def register_routes():
    app.register_blueprint(api)
    app.register_blueprint(view)


@api.route('/<string:title>/', methods=['GET'])
def get_game_by_title(title: str):
    game = Game.query.filter_by(title=title).first()

    return jsonify(game_schema.dump(game)) if game else jsonify(message="No game found by title: " + title), 404


@api.route('/', methods=['GET'])
def get_games():
    """
    Get a list of all of the games in the database.
    """
    games = Game.query.all()

    return jsonify(games_schema.dump(games)) if games else jsonify("No games found."), 404


@view.route('/')
class Games(MethodView):
    def get(self):
        """List games."""
        return render_template('games.html', games=Game.query.all())