#!/usr/bin/env python3
from app import db
from src.model.user import User
from src.model.game import Game
from marshmallow import Schema, fields


class UserCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), index=True, nullable=False)

    user = db.relationship('User', foreign_keys='UserCollection.user_id')
    game = db.relationship('Game', foreign_keys='UserCollection.game_id')

    def __repr__(self):
        return '<UserCollection {}>'.format(self.username)


class UserCollectionSchema(Schema):
    user_id = fields.Int()
    game_id = fields.Int()


class UserCollectionQueryArgsSchema(Schema):
    user_id = fields.Integer()
    game_id = fields.Integer()
