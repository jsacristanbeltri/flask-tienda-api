from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy
from models.SharedModels import db


class Language(db.Model):
    __tablename__ = "language"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    username = db.relationship('User')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
            return f'<Language "{self.name}">'

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name
        }