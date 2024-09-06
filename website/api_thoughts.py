from flask import Blueprint

api_thoughts = Blueprint('api_thoughts', __name__)

"""
TODO
1. get latest posts
2. get top rated posts
3. get most liked posts
4. get a users posts
"""

@api_thoughts.route('/')
def home():
    return {'message': 'Hello, World!'}

