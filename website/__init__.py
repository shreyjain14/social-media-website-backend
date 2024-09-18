from flask import Flask
from os import path, getenv
from dotenv import load_dotenv
from .extentions import db, bcrypt, cors, jwt

load_dotenv('/.env')


def create_app():
    app = Flask(__name__)

    # app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = getenv('JWT_SECRET')

    # extensions initialization
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # creating db if not exists
    from . import models

    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()

    # registering blueprints
    from .api_auth import api_auth
    from .api_thoughts import api_thoughts

    app.register_blueprint(api_auth, url_prefix='/auth/')
    app.register_blueprint(api_thoughts, url_prefix='/thoughts/')

    return app
