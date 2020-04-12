#!/user/bin/env python3
from app import db
from marshmallow import Schema
from sqlalchemy import Column, Integer


class Game(db.Model):
    id = Column(Integer, primary_key=True)
    bgg_id = Column(Integer, index=True, unique=True, nullable=False)
    title = Column(db.String(256), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Game {}>'.format(self.title)


class GameSchema(Schema):
    class Meta:
        fields = ('id', 'bgg_id', 'title')


game_schema = GameSchema()
games_schema = GameSchema(many=True)
