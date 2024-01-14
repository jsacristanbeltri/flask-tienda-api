from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy
from models.SharedModels import db

user_roles = db.Table('user_role',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                    )

class Role(db.Model):
        __tablename__ = 'role'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)