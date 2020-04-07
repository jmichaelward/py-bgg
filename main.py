#!/usr/bin/env python3
from flask import make_response, render_template
from setup import app
from src.routes import api, view

app.register_blueprint(api.routes)
app.register_blueprint(view.routes)


@app.errorhandler(404)
def show_404(message):
    return make_response(render_template('404.html', message=message), 404)


if __name__ == '__main__':
    app.run()
