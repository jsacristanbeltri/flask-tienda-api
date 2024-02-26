from .default import *
import os

database_url = os.environ.get('DATABASE_URL')
database_user = os.environ.get('DATABASE_USERNAME')
database_pass = os.environ.get('DATABASE_PASSWORD')

APP_ENV = APP_ENV_LOCAL
SQLALCHEMY_DATABASE_URI = 'postgresql://' + database_user + ':' + database_pass + '@' + database_url
