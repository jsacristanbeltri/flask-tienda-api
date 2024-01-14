from flask import Blueprint, abort, request, jsonify, make_response
from models.UserModel import User
from models.SharedModels import db
from services.UserService import UserService

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_users(): 
    users = UserService.get_users() 
    return jsonify(users)

@users.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = UserService.get_user(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404
    

@users.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if data['username'] is None or data['password'] is None:
        abort(400)
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
    updated_user = User(request.json['username'], request.json['password'], request.json['fullname'])
    user = UserService.update_user(id,updated_user)
    return jsonify(user)

@users.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    UserService.delete_user(id)
    return make_response('User deleted',200)
