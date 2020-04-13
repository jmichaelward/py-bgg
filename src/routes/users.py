from app import db, app
from flask import jsonify, request, render_template, redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from src.bgg_api import BggApi
from src.model.user import User, user_schema, users_schema, user_game_collection, games_collection_schema
from src.template.form import AddUserForm
from src.routes.view import template_routes
from src.routes.users_collection import get_collection
import sqlalchemy.orm.exc as error


api = Blueprint('users_api', 'users_api', url_prefix='/api/v1/users', description="Users API")
view = Blueprint('users', 'users',
                 url_prefix='/users', description='Operations on users', template_folder='templates')


def register_routes():
    app.register_blueprint(view)
    app.register_blueprint(api)


@view.route('/')
class Users(MethodView):
    def get(self):
        """List users."""
        return render_template('users.html', users=User.query.all())


@view.route('/<username>/')
class UsersById(MethodView):
    def get(self, username: str):
        """Get User by username"""
        try:
            user = db.session.query(User).filter(User.username == username).one()
            collection = get_collection(user)

            return render_template('user-profile.html', user=user, collection=collection)
        except error.NoResultFound:
            return render_template('404.html', message="Could not find user: " + username)


@template_routes.route('/add-user/', methods=['GET', 'POST'])
class UsersAdd(MethodView):
    def get(self):
        return render_template('add-user.html', form=self.user_form(request))

    def post(self):
        username = request.form.get('username')
        response = self.api_handle_add(username)

        if isinstance(response, User):
            return redirect('/users/' + username)

        return render_template('add-user.html', form=self.user_form(request))

    def user_form(self, request):
        return AddUserForm(request.form)

    def api_handle_add(self, username: str):
        user = db.session.query(User).filter(User.username == username).one_or_none()

        if isinstance(user, User):
            return user

        response, userdata = BggApi().get_json('user?name=' + username)

        if not userdata['user']['@id']:
            return {"status": 404}

        user = User(username=userdata['user']['@name'], bgg_id=userdata['user']['@id'])

        user_exists = db.session.query(User).filter(User.username == user.username).one_or_none()

        if user_exists:
            return user

        db.session.add(user)
        db.session.commit()

        return user


@api.route('/', methods=['GET'])
def get_users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    users = User.query.all()

    return jsonify(users_schema.dump(users)) if users else jsonify(message="No users found."), 404


@api.route('/<username>/')
def get_user(username: str):
    """
    Get information about a given user.
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify(message="No user exists for username: " + username), 404

    return jsonify(user_schema.dump(user))




