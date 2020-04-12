# Users handler.
from app import db
from sqlalchemy import exc
from src.model.user import User, games_collection
from src.model.game import Game
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
    user = db.session.query(User).filter(User.username == username).one_or_none()

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


def api_handle_collection_add(user: User):
    collection = get_collection(user)

    if collection:
        return collection

    response, userdata = get_bgg_json(bgg_base_url + 'collection?username=' + user.username)

    if 200 != response.status_code:
        return get_collection_response(response)

    games = userdata['items']['item'] if "item" in userdata['items'] else []

    if 0 == len(games):
        return []

    for game in games:
        new_game = create_game(Game(bgg_id=game['@objectid'], title=game['name']['#text']))
        add_to_collection(user, new_game)

    return get_collection(user)


def get_collection(user: User):
    return db.session.query(Game).join(games_collection).filter_by(user_id=user.id).all()


def add_to_collection(user: User, game: Game):
    if not db.session.query(games_collection).filter_by(user_id=user.id).filter_by(game_id=game.id).first():
        games_collection.update().values(user_id=user.id, game_id=game.id)


def create_game(game: Game):
    """
    Insert a game into the database.
    """
    existing_game = Game.query.filter_by(bgg_id=game.bgg_id).first()

    if existing_game:
        return existing_game

    db.session.add(game)
    db.session.commit()
    db.session.close()

    return game


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
