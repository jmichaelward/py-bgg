#!/usr/bin/env python3
from app import db
from marshmallow import Schema
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from .user_game_collection import user_game_collection, UserGameCollectionSchema


class User(db.Model):
    id = Column(Integer, primary_key=True)
    bgg_id = Column(Integer, index=True, unique=True, nullable=False)
    username = Column(String(256), index=True, unique=True, nullable=False)

    user_game_collection = relationship(
        'Game',
        secondary=user_game_collection,
        backref=backref('user')
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserSchema(Schema):
    class Meta:
        fields = ('id', 'bgg_id', 'username')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
games_collection_schema = UserGameCollectionSchema()
