#!/usr/bin/env python3
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from marshmallow import Schema


class UserGameCollectionSchema(Schema):
    class Meta:
        fields = ('id', 'user_id', 'game_id', 'title')


user_game_collection = Table(
    'user_game_collection',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True)
)
