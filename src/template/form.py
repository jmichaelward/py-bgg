#!/usr/bin/env python3
from wtforms import Form, validators, StringField


class ReusableForm(Form):
    """
    Reusable form mockup.

    This is based on https://pythonspot.com/flask-web-forms/. This seems pretty outdated, so I should
    investigate other solutions. The wtforms module is throwing some warning messages when starting
    up the server.
    """
    username = StringField('Username:', validators=[validators.required()])

    def __init__(self, form):
        super(ReusableForm, self).__init__()
        self.form = form
