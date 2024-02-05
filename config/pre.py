from .default import *
import os

database_url = os.environ.get('DATABASE_URL')
database_user = os.environ.get('DATABASE_USERNAME')
database_pass = os.environ.get('DATABASE_PASSWORD')

print('database_url: ' + database_url)
print('database_user: ' + database_user)
print('database_pass: ' + database_pass)

APP_ENV = APP_ENV_LOCAL
SQLALCHEMY_DATABASE_URI = 'postgresql://' + database_user + ':' + database_pass + '@' + database_url
#SQLALCHEMY_DATABASE_URI = 'postgresql://jsacristan:jsdutySDS27781doop@192.168.1.100:5432/listin_py_flask'
#print('alchemy: ' + SQLALCHEMY_DATABASE_URI)
