#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def create_form_from_request(request):
    return AddUserForm(request.form)


class AddUserForm(FlaskForm):
    """
    Reusable form mockup.

    This is based on https://pythonspot.com/flask-web-forms/. This seems pretty outdated, so I should
    investigate other solutions. The wtforms module is throwing some warning messages when starting
    up the server.
    """
    username = StringField('Username:', validators=[DataRequired()])
    submit = SubmitField('Add User')

    def __init__(self, form):
        super(AddUserForm, self).__init__()
        self.form = form
