from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy
from models.SharedModels import db
from models.TagModel import user_tag
from models.RoleModel import user_roles
from werkzeug.security import generate_password_hash, check_password_hash
import time
import jwt
from flask import current_app
from flask_login import (UserMixin)

#@RBAC.as_user_model
class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)
    fullname = Column(String, unique=True, index=True)
    language_id = Column(String, ForeignKey('language.id'))
    tags = db.relationship('Tag', secondary=user_tag, backref='user')
    roles = db.relationship('Role', secondary=user_roles, backref='user')


    def __init__(self, username, password, fullname, language):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.language_id = language

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, password={self.password}, fullname={self.fullname}, language_id={self.language_id}, tags={self.tags}, roles={self.roles})>'
    
    def to_JSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'fullname': self.fullname,
            'language': self.language_id,
            'tags': [tag.name for tag in self.tags],
            'roles': [role.name for role in self.roles]
        }
    
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_auth_token(self, expires_in = 600):
        return jwt.encode(
            { 'id': self.id, 'username': self.username, 'exp': time.time() + expires_in }, 
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token,current_app.config['SECRET_KEY'],
            algorithms=['HS256'])
            print('token detected, decoding...')
            return User.query.get(data['id'])
        except Exception as ex:
            print('exception: ' + str(ex))
            return 
        
    @staticmethod
    def get_token_auth_header(request):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return False, "Authorization header is expected"

        parts = auth.split()

        if parts[0].lower() != "bearer":
            return False, "Authorization header must start with Bearer"
        elif len(parts) == 1:
            return False, "Token not found"
        elif len(parts) > 2:
            return False, "Authorization header must be Bearer token"

        token = parts[1]
        return token, ''
        