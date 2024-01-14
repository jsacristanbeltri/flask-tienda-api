from flask import Blueprint, abort, request, jsonify, make_response, g
from flask_security import roles_accepted
from models.UserModel import User
from models.SharedModels import db
from flask_httpauth import HTTPBasicAuth

aut = Blueprint('aut', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token,password): 
    # first try token
    user = User.verify_auth_token(username_or_token)
    # then check for username and password pair
    if not user:
        print('token do not detected, checking username/password')
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
             return False
    g.user = user
    return True

@aut.route('/api/login')
@auth.login_required
def get_token():
    token = g.user.generate_auth_token(600)
    print('token generated: ' + token)
    return jsonify({ 'token': token, 'duration': 600 })


@aut.route('/api/dothisUser', methods=['GET'])
@auth.login_required
def test_user_authorization():
    return jsonify({ 'message':'It is done user {}'.format(g.user.username) })

@aut.route('/api/dothisAdmin', methods=['GET'])
@auth.login_required
def test_admin_authorization():
    return jsonify({ 'message':'It is done admin {}'.format(g.user.username) })