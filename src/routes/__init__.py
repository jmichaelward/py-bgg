#!/usr/bin/env python3
from flask import Flask


def load(app: Flask):
    """Load application routes."""
    from . import api
    from . import view

    app.register_blueprint(api.routes)
    app.register_blueprint(view.routes)
    app.register_blueprint(view.user_routes)

