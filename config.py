import os

__basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLE = True
SECRET_KEY = "a secret"

DATABASE_FILE = "tempdb.sqlite"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(__basedir,DATABASE_FILE)
SQLALCHEMY_ECHO = True