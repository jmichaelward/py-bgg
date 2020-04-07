#!/usr/bin/env python3
from setup import app, db
from src.routes import api, view

app.register_blueprint(api.routes)
app.register_blueprint(view.routes)


if __name__ == '__main__':
    app.run()
