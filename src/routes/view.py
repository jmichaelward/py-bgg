#!/usr/bin/env python3
from flask import request, redirect, render_template
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import db
from src.model.user import User, UserSchema, UserQueryArgsSchema
from src.api import users
from src.template.form import AddUserForm
from src.api.users import api_handle_collection_add

routes = Blueprint('view', __name__, template_folder='templates')
user_routes = Blueprint('users', 'users',
                        url_prefix='/users', description='Operations on users', template_folder='templates')


@user_routes.route('/')
class Users(MethodView):
    def get(self):
        """List users."""
        return render_template('users.html', users=User.query.all())


@user_routes.route('/<username>')
class UsersById(MethodView):
    def get(self, username: str):
        """Get User by username"""
        user = db.session.query(User).filter(User.username == username).one()

        return render_template('user-profile.html', user=user, collection=[])


@routes.route('/add-user', methods=['GET', 'POST'])
def add_users():
    """
    Add user form.

    This loads a basic input form if it's a GET request, or re-renders it again
    if we received a non-200 response from the server.

    The "request" is just a connection to the database, which also makes a call to BoardGameGeek behind
    the scenes of a record is not present in the database.
    """
    form = AddUserForm(request.form)

    if request.method == 'GET':
        return render_template('add-user.html', form=form)

    username = request.form.get('username')
    response = users.api_handle_add(username)

    if isinstance(response, User):
        return redirect('/users/' + username)

    return render_template('add-user.html', form=form)


# @routes.route('/users/<username>')
# def show_user_profile(username):
#     user = User.query.get(username)
#
#     if not isinstance(user, User):
#         return render_template('404.html', message="Could not find user: " + username)
#
#     # @TODO Fix collection processing with new database ORM.
#     # collection = db.get_user_collection(user['username'])
#     #
#     # if 0 == len(collection):
#     #     collection = api_handle_collection_add(username)
#
#     """
#     Front-end template for a user page. This could maybe show a list of the user's games?
#     """
#     return render_template('user-profile.html', user=user, collection=[])
#
#
# @routes.route('/games')
# def show_games():
#     games = db.get_games()
#     return render_template('games.html', games=sorted(games))
#
#
@routes.route('/')
def index():
    """
    The main page is just going to show links to the various API routes.
    """
    app = {
        "title": "Python BoardGameGeek!"
    }

    return render_template('main.html', app=app)
