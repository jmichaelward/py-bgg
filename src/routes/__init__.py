#!/usr/bin/env python3
from . import view, users, games, users_collection


modules = [
    view,
    users,
    games,
    users_collection
]


def load_modules():
    for module in modules:
        module.register_routes()


load_modules()
