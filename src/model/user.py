#!/usr/bin/env python3
from app import db
from marshmallow import Schema, fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bgg_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    username = db.Column(db.String(256), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserSchema(Schema):
    bgg_id = fields.Int()
    username = fields.Str()


class UserQueryArgsSchema(Schema):
    username = fields.String()
