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

    if user:
        return {
            "id": user['bgg_id'],
            "username": user['username'],
            "status": 200
        }

    response, userdata = get_bgg_json(bgg_base_url + 'user?name=' + username)

    if not userdata['user']['@id']:
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

    if 200 != response.code:
        return get_collection_response(response)

    games = userdata['items']['item'] if "item" in userdata['items'] else []

    if 0 == len(games):
        return []

    for game in games:
        db.create_game(game)
        db.add_game_to_collection(game, user)

    return db.get_user_collection(username)


def get_collection_response(response):
    """
    Get an appropriate response for a non-200 response to the /collections endpoint.
    :param response:
    :return:
    """
    if 202 == response.code:
        return []  # @TODO Figure out how to handle BGG's response that it's processing user data.
    elif 404 == response.code:
        return []  # @TODO Figure out whether this is actually a code BGG returns and what to do in this case.

    return []  # @TODO Figure out whether there are other responses to handle. There certainly are.
