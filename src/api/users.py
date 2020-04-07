# Users handler.
from setup import db
from urllib.request import urlopen
import xmltodict

bgg_base_url = 'https://boardgamegeek.com/xmlapi2/'


def get_bgg_json(url):
    """
    Get a JSON response from the BoardGameGeek api.

    :param url:
    :return:
    """
    response = urlopen(url)
    return response, xmltodict.parse(response.read())


def api_handle_add(username: str):
    user = db.get_user(username)

    if len(user) == 1:
        return {
            "id": user[0]['bgg_id'],
            "username": user[0]['username'],
            "status": 200
        }

    response, userdata = get_bgg_json(bgg_base_url + 'user?name=' + username)

    if userdata['user']['@id'] == '':
        return {"status": 404}

    user = {
        "id": userdata['user']['@id'],
        "username": userdata['user']['@name'],
        "status": response.code
    }

    return user if db.create_user(user) else {"status": 500}


def api_handle_collection_add(username: str):
    user = api_handle_add(username)

    if 200 != user['status']:
        return []  # @TODO User not found - handle more elegantly.

    response, userdata = get_bgg_json(bgg_base_url + 'collection?username=' + username)
    games = userdata['items']['item']

    if 0 == len(games):
        return []

    for game in games:
        db.create_game(game)
        db.add_game_to_collection(game, user)

    return db.get_user_collection(username)



