from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# routes need app, models need db
from cryptoapi import routes, models
