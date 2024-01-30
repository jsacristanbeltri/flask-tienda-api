import logging
from flask import Blueprint, abort, request, jsonify, make_response
from models.UserModel import User
from models.SharedModels import db
from services.UserService import UserService
from werkzeug.exceptions import NotFound, BadRequest

users = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

@users.route('/users', methods=['GET'])
def get_users(): 
    logger.info("IN get all user")
    users = UserService.get_users() 
    return jsonify(users)

@users.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    logger.info('IN get user with id {}'.format(id))
    user = UserService.get_user(id)
    if user:
        return jsonify(user)
    else:
        #return jsonify({'message': 'User not found'}), 404
        raise NotFound('User with id {} not found'.format(id))
    

@users.route('/users', methods=['POST'])
def add_user():
    logger.info('IN add user, request:  {}', request)
    data = request.json
    if 'username' not in data or not data['username'] or data['username'] is None:
        raise BadRequest("Username is missing or empty")
    
    if 'password' not in data or not data['password'] or data['password'] is None:
        raise BadRequest("Password is missing or empty")
    
    new_user = User(
        username=data['username'],
          password=data['password'],
            fullname=data['fullname'],
              language=data['language'])
    userDb = UserService.add_user(new_user, data.get('tags', []))
    if userDb:
        return jsonify(userDb), 201
    else:
        return jsonify({'message': 'Error adding user'}), 500

@users.route('/<int:id>', methods=['PUT'])
def update_user(id):
    logger.info('IN update user with id {}, request: {}'.format(id, request))
    updated_user = User(
        request.json['username'],
          request.json['password'],
            request.json['fullname'],
                request.json['language'])
    user = UserService.update_user(id,updated_user, request.json['tags'])
    return jsonify(user)

@users.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    logger.info('IN delete user with id {}'.format(id))
    UserService.delete_user(id)
    return make_response('User deleted',200)
