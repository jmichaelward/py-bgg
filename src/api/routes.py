#!/usr/bin/env python3
from flask import jsonify, Blueprint

api = Blueprint('api', __name__)


@api.route('/api/v1/users', methods=['GET'])
def users():
    from main import db

    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    return jsonify(db.get_users())
