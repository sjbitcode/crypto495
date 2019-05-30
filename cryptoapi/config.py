import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'cryptodb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PAGINATION_LIMIT = 50
    ROOT_URL = os.environ.get('ROOT_URL', 'ROOT_URL')
