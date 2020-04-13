#!/usr/bin/env python3
from app import db
from marshmallow import Schema
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref


games_collection = Table(
    'user_game_collection',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True)
)


class UserGameCollectionSchema(Schema):
    class Meta:
        fields = ('id', 'user_id', 'game_id', 'title')


class User(db.Model):
    id = Column(Integer, primary_key=True)
    bgg_id = Column(Integer, index=True, unique=True, nullable=False)
    username = Column(String(256), index=True, unique=True, nullable=False)

    user_game_collection = relationship(
        'Game',
        secondary=games_collection,
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
