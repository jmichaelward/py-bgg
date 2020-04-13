#!/usr/bin/env python3
from flask import Flask, make_response, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import src.routes
import src.model


@app.errorhandler(404)
def show_404(message):
    return make_response(render_template('404.html', message=message), 404)


if __name__ == '__main__':
    app.run()
