from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy
from models.SharedModels import db

user_tag = db.Table('user_tag',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Tag "{self.name}">' 
    
    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name
        }