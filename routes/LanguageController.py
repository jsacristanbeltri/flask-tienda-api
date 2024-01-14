from flask import Blueprint, request, jsonify
from models.LanguageModel import Language
from services.LanguageService import LanguageService

languages = Blueprint('languages', __name__)

@languages.route('/languages', methods=['GET'])
def get_languages():
    languages = LanguageService.get_all_languages()
    return jsonify(languages)

@languages.route('/languages/<string:id>', methods=['GET'])
def get_language(id):
    language = LanguageService.get_language_by_id(id)
    if language:
        return jsonify(language)
    else:
        return jsonify({'message': 'Language not found'}), 404

@languages.route('/languages', methods=['POST'])
def add_language():
    data = request.json
    new_language = Language(id=data['id'], name=data['name'])
    language = LanguageService.add_language(new_language)
    if language:
        return jsonify(language), 201
    else:
        return jsonify({'message': 'Error saving language'}), 500

@languages.route('/languages/<string:id>', methods=['PUT'])
def update_language(id):
    data = request.json
    updated_language = Language(id=id, name=data['name'])
    language = LanguageService.update_language(updated_language)
    return jsonify(language)

@languages.route('/languages/<string:id>', methods=['DELETE'])
def delete_language(id):
    LanguageService.delete_language(id)
    return jsonify({'message': 'Language deleted'})
