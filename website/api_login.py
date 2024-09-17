import sqlite3
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .extentions import bcrypt, db
from .models import User, Following

api_login = Blueprint('api_login', __name__)


@api_login.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return {
        # Log user out
    }


@api_login.route('/login-user', methods=['GET', 'POST'])
def login_data():
    user = User.query.filter_by(
        # username=username_from_api
    ).first()
    if user:
        if bcrypt.check_password_hash(
                user.password,
                # form.password.data
        ):
            login_user(user)
            return {
                # Log user in
            }
        else:
            return {
                # Password incorrect
            }
    else:
        return {
            # Username not found
        }


def validate_username(username):
    if User.query.filter_by(
            username=username
    ).first():
        return 1
    else:
        return 0


@api_login.route('/register-user', methods=['GET', 'POST'])
def register():
    try:
        if validate_username(
                # username
        ):
            return {
                # Username already exists
            }

        else:
            hashed_password = bcrypt.generate_password_hash(
                # form.password.data
            )
            new_user = User(
                # username=form.username.data.lower(), 
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            new_Fuser = Following(
                # form.username.data.lower()
            )
            db.session.add(new_Fuser)
            db.session.commit()

            return {
                # User created
            }

    except sqlite3.IntegrityError:
        return {
            # Username already exists
        }
