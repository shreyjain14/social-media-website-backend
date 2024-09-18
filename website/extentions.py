from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

cors = CORS()
bcrypt = Bcrypt()
db = SQLAlchemy()
