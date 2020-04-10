# Users handler.
from app import db
from sqlalchemy import exc
from src.model.user import User
import requests
import xmltodict

bgg_base_url = 'https://boardgamegeek.com/xmlapi2/'


def get_bgg_json(url):
    """
    Get a JSON response from the BoardGameGeek api.

    :param url:
    :return:
    """
    response = requests.request('GET', url)
    return response, xmltodict.parse(response.content)


def api_handle_add(username: str):
    user = User.query.get(username)

    if isinstance(user, User):
        return user

    response, userdata = get_bgg_json(bgg_base_url + 'user?name=' + username)

    if not userdata['user']['@id']:
        return {"status": 404}

    user = User(username=userdata['user']['@name'], bgg_id=userdata['user']['@id'])

    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:  # Ignore duplicate entries.
        return user

    return user


def api_handle_collection_add(username: str):
    user = api_handle_add(username)

    if 200 != user['status']:
        return []  # @TODO User not found - handle more elegantly.

    response, userdata = get_bgg_json(bgg_base_url + 'collection?username=' + username)

    if 200 != response.status_code:
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
    if 202 == response.status_code:
        return []  # @TODO Figure out how to handle BGG's response that it's processing user data.
    elif 404 == response.status_code:
        return []  # @TODO Figure out whether this is actually a code BGG returns and what to do in this case.

    return []  # @TODO Figure out whether there are other responses to handle. There certainly are.
