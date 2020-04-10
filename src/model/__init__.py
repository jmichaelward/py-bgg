#!/usr/bin/env python3
from flask import Flask


def load(app: Flask):
    """Load the app models."""
    from . import user
    from . import game
    from . import user_collection
