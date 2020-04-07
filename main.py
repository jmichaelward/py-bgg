#!/usr/bin/env python3
from flask import Flask, json, jsonify, render_template, escape, request, redirect, flash
from src import db as Database
from src.api.users import api_handle_add
from wtforms import Form, TextAreaField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

db = Database.Database()
db.connect()


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
    response = api_handle_add(username)

    if 200 == response['status']:
        return redirect('/users/' + username)

    return render_template('add-user.html', form=form)


@app.route('/api/v1/users')
def users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    return jsonify(db.get_users())


@app.route('/users/<username>')
def show_user_profile(username):
    """
    Front-end template for a user page. This could maybe show a list of the user's games?
    """
    return 'User %s' % escape(username)


@app.route('/')
def main():
    """
    The main page is just going to show links to the various API routes.
    """
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
