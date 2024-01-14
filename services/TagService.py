from models.TagModel import Tag
from models.SharedModels import db

class TagService:
    @staticmethod
    def get_all_tags():
        tags = Tag.query.all()
        return [tag.to_JSON() for tag in tags]

    @staticmethod
    def get_tag_by_id(id):
        tag = Tag.query.get(id)
        return tag.to_JSON() if tag else None

    @staticmethod
    def add_tag(new_tag):
        db.session.add(new_tag)
        db.session.commit()
        return new_tag.to_JSON()

    @staticmethod
    def update_tag(updated_tag):
        tag = Tag.query.get(updated_tag.id)
        if tag:
            tag.name = updated_tag.name
            db.session.commit()
            return tag.to_JSON()
        else:
            return None

    @staticmethod
    def delete_tag(id):
        tag = Tag.query.get(id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
