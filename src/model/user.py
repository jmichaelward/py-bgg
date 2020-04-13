#!/usr/bin/env python3
from app import db
from marshmallow import Schema
from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.orm import relationship, backref
from .user_game_collection import user_game_collection, UserGameCollectionSchema
from .game import Game
from src.bgg_api import BggApi


class User(db.Model):
    id = Column(Integer, primary_key=True)
    bgg_id = Column(Integer, index=True, unique=True, nullable=False)
    username = Column(String(256), index=True, unique=True, nullable=False)

    user_game_collection = relationship(
        'Game',
        secondary=user_game_collection,
        backref=backref('user')
    )

    def get_collection(self):
        return Game.query.join(
            user_game_collection
        ).filter(user_game_collection.c.user_id == self.id).all()

    def update_collection(self):
        response, userdata = BggApi().get_json('collection?username=' + self.username)

        if 200 != response.status_code:
            return

        games = userdata['items']['item'] if "item" in userdata['items'] else []

        if 0 == len(games):
            return

        for game in games:
            new_game = Game(bgg_id=game['@objectid'], title=game['name']['#text'])
            created = new_game.create_record()

            if not isinstance(created, Game):
                continue

            self.add_to_collection(created)

    def add_to_collection(self, game: Game):
        if game and not self.has_game(game):
            self.add_game_to_user_collection(game)

    def add_game_to_user_collection(self, game: Game):
        result = db.session.execute(
            user_game_collection.insert(), {"user_id": self.id, "game_id": game.id}
        )

        db.session.commit()
        return result

    def has_game(self, game: Game):
        return db.session.execute(
            user_game_collection.select().where(
                and_(
                    user_game_collection.c.user_id == self.id,
                    user_game_collection.c.game_id == game.id
                )
            )
        ).fetchone()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserSchema(Schema):
    class Meta:
        fields = ('id', 'bgg_id', 'username')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
games_collection_schema = UserGameCollectionSchema()
