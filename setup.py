from flask import Flask
from src.db import Database

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

db = Database()
db.connect()
