from flask import Flask
from config import Config
from src.db import Database

app = Flask(__name__)
app.config.from_object(Config)

db = Database()
db.connect()
