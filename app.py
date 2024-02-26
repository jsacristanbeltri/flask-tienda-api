# configura la app
import os
import logging
from flask import Flask,jsonify
from routes.UserController import users
from routes.LanguageController import languages
from routes.TagsController import tag
from routes.AuthController import aut
from models.SharedModels import db
from datetime import datetime
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from celery import Celery

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
app.config.from_object(os.getenv('APP_SETTINGS_MODULE'))

db.init_app(app)

app.register_blueprint(users)
app.register_blueprint(languages)
app.register_blueprint(tag)
app.register_blueprint(aut)

def configure_logging(app):
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

# custom logging
configure_logging(app)

def register_error_handlers(app):

    @app.errorhandler(400)
    def error_400_handler(e):
        return jsonify({'timestamp': datetime.now().isoformat(),'message': str(e)}), 400

    @app.errorhandler(404)
    def error_404_handler(e):
        return jsonify({'timestamp': datetime.now().isoformat(),'message': str(e)}), 404
    
    @app.errorhandler(500)
    def error_500_handler(e):
        return jsonify({'timestamp': datetime.now().isoformat(),'message': str(e)}), 404
    
# Custom error handlers
register_error_handlers(app)

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@celery.task
def add(x, y):
    return x + y