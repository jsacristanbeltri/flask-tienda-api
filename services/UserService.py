from flask import abort, jsonify
from models.SharedModels import db
from models.TagModel import Tag
from models.UserModel import User
from models.RoleModel import Role
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError


class UserService():
    @classmethod
    def get_users(cls): 
        try:
            users = User.query.all()
            response = []
            for user in users: response.append(user.to_JSON())
            return response
        except Exception as ex: 
            print('error: ' + str(ex))
            raise InternalServerError(ex)

    @classmethod
    def get_user(self,id):
        try:
            user = User.query.filter_by(id = id).first()
            return user
        except Exception as ex: 
            print('error: ' + str(ex))
            raise InternalServerError(ex)

    @classmethod
    def add_user(cls, new_user, tags):
        try:
            if User.query.filter_by(username = new_user.username).first():
                raise BadRequest('The user {} already exists on database '.format(new_user.username))
            if tags:
                new_user.tags.extend(Tag.query.filter(Tag.id.in_(tags)).all())
            role = Role.query.filter_by(name='User').first()
            new_user.roles.append(role)
            new_user.hash_password(new_user.password)
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_JSON()
        except Exception as ex: 
            print('error: ' + str(ex))
            raise InternalServerError(ex)

    @classmethod
    def delete_user(self,id):
        try:
            userDb = User.query.filter_by(id = id).first()
            if not userDb: 
                raise NotFound('User with id {} not found'.format(id))       
            db.session.delete(userDb)
            db.session.commit()  
        except NotFound as ex: 
            raise ex       
        except Exception as ex:
            print('error: ' + str(ex))
            raise InternalServerError(ex)

    @classmethod
    def update_user(self,id,new_user, tags): 
        try:           
            userDb = User.query.filter_by(id = id).first()
            if not userDb: 
             raise NotFound('User with id {} not found'.format(id))
              
            if tags:
                new_user.tags.extend(Tag.query.filter(Tag.id.in_(tags)).all())

            userDb.username = new_user.username
            userDb.password = new_user.password
            userDb.fullname = new_user.fullname
            userDb.tags = new_user.tags
            db.session.add(userDb)
            db.session.commit()
            return userDb.to_JSON()
        
        except NotFound as ex: 
            raise ex      
        except Exception as ex: 
            print('error: ' + str(ex))
            raise InternalServerError(ex)
