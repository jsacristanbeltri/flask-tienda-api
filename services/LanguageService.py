from models.LanguageModel import Language
from models.SharedModels import db

class LanguageService:
    @staticmethod
    def get_all_languages():
        languages = Language.query.all()
        return [language.to_JSON() for language in languages]

    @staticmethod
    def get_language_by_id(id):
        language = Language.query.get(id)
        return language.to_JSON() if language else None

    @staticmethod
    def add_language(new_language):
        try:
            db.session.add(new_language)
            db.session.commit()
            return new_language.to_JSON()
        except Exception as ex: 
            print('error: ' + str(ex))
        

    @staticmethod
    def update_language(updated_language):
        language = Language.query.get(updated_language.id)
        if language:
            language.name = updated_language.name
            db.session.commit()
            return language.to_JSON()
        else:
            return None

    @staticmethod
    def delete_language(id):
        language = Language.query.get(id)
        if language:
            db.session.delete(language)
            db.session.commit()
