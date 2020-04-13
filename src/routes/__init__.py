#!/usr/bin/env python3
from . import view, users, games


modules = [
    view,
    users,
    games
]


def load_modules():
    for module in modules:
        module.register_routes()


load_modules()
