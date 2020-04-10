#!/usr/bin/env python3
from flask import Flask, make_response, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import src.routes as routes
import src.model as models

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Load our routes.
routes.load(app)
models.load(app)


@app.errorhandler(404)
def show_404(message):
    return make_response(render_template('404.html', message=message), 404)


if __name__ == '__main__':
    app.run()
