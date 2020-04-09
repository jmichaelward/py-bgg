#!/usr/bin/env python3
from marshmallow import Schema, fields


class UserSchema(Schema):
    bgg_id = fields.Int()
    bgg_profile = fields.Str()
    username = fields.Str()
