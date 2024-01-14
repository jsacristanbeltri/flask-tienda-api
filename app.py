# configura la app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.RoleModel import Role
from models.UserModel import User
from routes.UserController import users
from routes.LanguageController import languages
from routes.TagsController import tag
from routes.AuthController import aut
from models.SharedModels import db

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"
           ] = "postgresql://jsacristan:jsdutySDS27781doop@localhost:5432/listin_py_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'use a random string to construct the hash'

db.init_app(app)


app.register_blueprint(users)
app.register_blueprint(languages)
app.register_blueprint(tag)
app.register_blueprint(aut)