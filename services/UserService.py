from flask import abort, jsonify
from models.SharedModels import db
from models.TagModel import Tag
from models.UserModel import User
from models.RoleModel import Role

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

    @classmethod
    def get_user(self,id):
        try:
            user = User.query.get_or_404(id)
            return user
        except Exception as ex: 
            print('error: ' + str(ex))

    @classmethod
    def add_user(cls, new_user, tags):
        try:
            # Check for existing users
            if User.query.filter_by(username = new_user.username).first():
                abort(400)
            if tags:
                new_user.tags.extend(Tag.query.filter(Tag.id.in_(tags)).all())
            role = Role.query.filter_by(name='User').first()
            print('role found: ' + role.name)
            new_user.roles.append(role)
            new_user.hash_password(new_user.password)
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_JSON()
        except Exception as ex: 
            print('error: ' + str(ex))

    @classmethod
    def delete_user(self,id):
        try:
            userDb = User.query.get_or_404(id)
            db.session.delete(userDb)
            db.session.commit()
        except Exception as ex: 
            print('error: ' + str(ex))

    @classmethod
    def update_user(self,id,new_user): 
        try:                
             userDb = User.query.get_or_404(id)
             userDb.username = new_user.username
             userDb.password = new_user.password
             userDb.fullname = new_user.fullname
             db.session.add(userDb)
             db.session.commit()
             return userDb
        except Exception as ex: 
            print('error: ' + str(ex))
