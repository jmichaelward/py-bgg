#!/user/bin/env python3
from app import db
from marshmallow import Schema, fields


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bgg_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    title = db.Column(db.String(256), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Game {}>'.format(self.title)


class GameSchema(Schema):
    bgg_id = fields.Int()
    title = fields.Str()


class GameQueryArgsSchema(Schema):
    title = fields.String()
