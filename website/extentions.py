from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

jwt = JWTManager()
cors = CORS()
db = SQLAlchemy()
