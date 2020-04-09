#!/usr/bin/env python3


class User:
    def __init__(self, bgg_id: int, username: str):
        self.bgg_id = bgg_id
        self.bgg_profile = "https://boardgamegeek.com/user/" + username
        self.username = username
