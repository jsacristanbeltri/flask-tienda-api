from flask import Blueprint, request, jsonify
from models.TagModel import Tag
from services.TagService import TagService
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

tag = Blueprint('tag', __name__)

@tag.route('/tags', methods=['GET'])
def get_tags():
    tags = TagService.get_all_tags()
    return jsonify(tags)

@tag.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    tag = TagService.get_tag_by_id(id)
    if tag:
        return jsonify(tag)
    else:
        raise NotFound('Tag with id {} not found'.format(id))

@tag.route('/tags', methods=['POST'])
def add_tag():
    data = request.json
    new_tag = Tag(name=data['name'])
    tag = TagService.add_tag(new_tag)
    return jsonify(tag), 201

@tag.route('/tags/<int:id>', methods=['PUT'])
def update_tag(id):
    data = request.json
    updated_tag = Tag(id=id, name=data['name'])
    tag = TagService.update_tag(updated_tag)
    return jsonify(tag)

@tag.route('/tags/<int:id>', methods=['DELETE'])
def delete_tag(id):
    TagService.delete_tag(id)
    return jsonify({'message': 'Tag deleted'})

# Puedes agregar más rutas según tus necesidades
