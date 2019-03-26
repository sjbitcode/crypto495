import json
import os

from cryptoapi import db
from .config import BASEDIR
from .models import Crypto

def get_data():
    data_file = os.path.join(BASEDIR, 'coinmarketcap', 'db_metadata.json')
    with open(data_file) as f:
        return json.load(f)

def seed():
    data = get_data()
    data = list(data.values())

    # source: https://gist.github.com/shrayasr/5df96d5bc287f3a2faa4
    db.engine.execute(Crypto.__table__.insert(), data)
