#!/usr/bin/env python3
from setup import app, db
from flask import render_template, request, redirect, make_response
from wtforms import Form, validators, StringField
from src.api import users
from src.routes import api

app.register_blueprint(api.routes)


class ReusableForm(Form):
    """
    @TODO A real reusable form wouldn't go in the main project file.
    This is based on https://pythonspot.com/flask-web-forms/.
    """
    username = StringField('Username:', validators=[validators.required()])

    def __init__(self, form):
        super(ReusableForm, self).__init__()
        self.form = form


@app.route('/add-user', methods=['GET', 'POST'])
def add_users():
    """
    Add user form.

    This loads a basic input form if it's a GET request, or re-renders it again
    if we received a non-200 response from the server.

    The "request" is just a connection to the database, which also makes a call to BoardGameGeek behind
    the scenes of a record is not present in the database.
    """
    form = ReusableForm(request.form)

    if request.method == 'GET':
        return render_template('add-user.html', form=form)

    username = request.form.get('username')
    response = users.api_handle_add(username)

    if 200 == response['status']:
        return redirect('/users/' + username)

    return render_template('add-user.html', form=form)


@app.route('/users/<username>')
def show_user_profile(username):
    user = db.get_user(username)

    if 0 == len(user):
        return render_template('404.html', message="Could not find user: " + username)
    """
    Front-end template for a user page. This could maybe show a list of the user's games?
    """
    return render_template('user-profile.html', user=user[0])


@app.errorhandler(404)
def show_404(message):
    return make_response(render_template('404.html', message=message), 404)


@app.route('/')
def main():
    """
    The main page is just going to show links to the various API routes.
    """
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
