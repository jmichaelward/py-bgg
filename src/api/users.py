# Users handler.
from main import db
from urllib.request import urlopen
import xmltodict

bgg_base_url = 'https://boardgamegeek.com/xmlapi2/'


def get_bgg_json(url):
    request = urlopen(url)
    return xmltodict.parse(request.read())


def api_handle_add(username: str):
    user = db.get_user(username)

    if len(user) == 1:
        return {
            "id": user[0]['bgg_id'],
            "username": user[0]['username'],
            "status": 200
        }

    request = urlopen(bgg_base_url + 'user?name=' + username)
    data = xmltodict.parse(request.read())

    if data['user']['@id'] == '':
        return {"status": 404}

    user = {
        "id": data['user']['@id'],
        "username": data['user']['@name'],
        "status": 200
    }

    return user if db.create_user(user) else {"status": 500}


def api_handle_collection_add(username: str):
    user = api_handle_add(username)

    if 200 != user['status']:
        return []  # @TODO User not found - handle more elegantly.

    data = get_bgg_json(bgg_base_url + 'collection?username=' + username)
    games = data['items']['item']

    if 0 == len(games):
        return []

    for game in games:
        db.create_game(game)
        db.add_game_to_collection(game, user)

    return db.get_user_collection(username)



