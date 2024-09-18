from flask import Flask
from os import path, getenv
from dotenv import load_dotenv
from .extentions import db, bcrypt, cors

load_dotenv('/.env')


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    from . import models

    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()

    from .api_login import api_login
    from .api_thoughts import api_thoughts

    app.register_blueprint(api_login, url_prefix='/login/')
    app.register_blueprint(api_thoughts, url_prefix='/thoughts/')

    return app
