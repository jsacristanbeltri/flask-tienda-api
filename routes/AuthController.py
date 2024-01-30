from flask import Blueprint, abort, request, jsonify, make_response, g, current_app
from models.UserModel import User
from models.SharedModels import db
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import jwt
import logging

aut = Blueprint('aut', __name__)
auth = HTTPBasicAuth()
logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token, msg = User.get_token_auth_header(request)
        if token == False:
            return { "error": msg }, 401
        try:
            user = User.verify_auth_token(token)
            if user: 
                print('token validated. Saving username {} on g... '.format(str(user.username)))
                g.user = user
        except Exception as e:
            return { "error": "Invalid Token" }, 401
        return f(*args, **kwargs)
    return decorator

def should_be_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if "Admin" not in [role.name for role in g.user.roles]:
                return jsonify({"error": "Invalid role, must be admin"}), 403
        except Exception as e:
            return jsonify({"error": "Invalid request"}), 403
  
        return f(*args, **kwargs)
    return decorator

def should_be_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if "User" not in [role.name for role in g.user.roles]:
                return jsonify({"error": "Invalid role, must be user"}), 403
        except Exception as e:
            return jsonify({"error": "Invalid request"}), 403
  
        return f(*args, **kwargs)
    return decorator

@aut.route('/api/login', methods=['POST'])
def login():
    logger.info('IN login user: ' + request.json['username'])
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Wrong username or password"}), 403
    else:
        token = user.generate_auth_token(600)
        g.user = user
        print('token generated: ' + token)
        return jsonify({ 'token': token, 'duration': 600 })
    
@aut.route('/api/dothis', methods=['GET'])
def test_user():
    return jsonify({ 'message':'It is done user without auth' })

@aut.route('/api/dothisUser', methods=['GET'])
@login_required
@should_be_user
def test_user_authorization():
    return jsonify({ 'message':'It is done user logged{}'.format(g.user.username) })

@aut.route('/api/dothisAdmin', methods=['GET'])
@login_required
@should_be_admin
def test_admin_authorization():
    return jsonify({ 'message':'It is done admin logged{}'.format(g.user.username) })

