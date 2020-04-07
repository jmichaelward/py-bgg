# Users handler.
from flask import jsonify
from main import db
from urllib.request import urlopen
import xmltodict

bgg_base_url = 'https://boardgamegeek.com/xmlapi2/'


def api_handle_add(username: str):
    user = db.get_user(username)

    if len(user) > 0:
        return {"status": 200}

    request = urlopen(bgg_base_url + 'user?name=' + username)
    data = xmltodict.parse(request.read())

    if data['user']['@id'] == '':
        return {"status": 404}

    user = {
        "id": data['user']['@id'],
        "username": data['user']['@name']
    }

    return {"status": 200} if db.create_user(user) else {"status": 500}
