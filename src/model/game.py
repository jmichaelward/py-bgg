#!/user/bin/env python3
from app import db
from marshmallow import Schema
from sqlalchemy import Column, Integer


class Game(db.Model):
    id = Column(Integer, primary_key=True)
    bgg_id = Column(Integer, index=True, unique=True, nullable=False)
    title = Column(db.String(256), index=True, nullable=False)

    def create_record(self):
        """
        Insert a game into the database.
        """
        existing_game = Game.query.filter_by(bgg_id=self.bgg_id).first()

        if existing_game:
            return existing_game

        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return '<Game {}>'.format(self.title)


class GameSchema(Schema):
    class Meta:
        fields = ('id', 'bgg_id', 'title')


game_schema = GameSchema()
games_schema = GameSchema(many=True)
