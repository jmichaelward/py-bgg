#!/usr/bin/env python3
from app import app
from flask import render_template
from flask_smorest import Blueprint

template_routes = Blueprint('view', __name__, url_prefix='/', template_folder='templates')


def register_routes():
    app.register_blueprint(template_routes)


@template_routes.route('/')
def index():
    """
    The main page is just going to show links to the various API routes.
    """
    details = {
        "title": "Python BoardGameGeek!"
    }

    return render_template('main.html', details=details)
