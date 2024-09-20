from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import Thought, Following
from flask_jwt_extended import jwt_required, current_user

api_thoughts = Blueprint('api_thoughts', __name__)


@api_thoughts.route('/create', methods=['POST'])
@jwt_required()
def create_thought():
    data = request.get_json()
    content = data.get('content')
    anonymous = data.get('anonymous', False)

    if not content:
        return jsonify({'message': 'Content is required'}), 400

    if anonymous:
        thought = Thought(content=content, date=datetime.now())
    else:
        thought = Thought(content=content, date=datetime.now(), user_id=current_user.username)

    following = Following.query.filter_by(username=current_user.username).first()
    if following:
        following.add_thought()
        following.save()

    thought.save()

    created_post = {
        'id': thought.id,
        'user_id': 'Anonymous' if anonymous else current_user.username,
        'content': content,
        'date': thought.date.isoformat()
    }

    return jsonify(created_post), 201


@api_thoughts.route('/get')
def get():

    thoughts = Thought.query.order_by(Thought.date.desc()).all()

    response = []

    for i in thoughts:
        response.append({
            'id': i.id,
            'content': i.content,
            'date': i.date,
            'user_id': i.user_id
        })

    return jsonify(response), 200


@api_thoughts.route('/get/<username>')
def get_user_thoughts(username):

    thoughts = Thought.query.filter_by(user_id=username).order_by(Thought.date.desc()).all()

    response = []

    for i in thoughts:
        response.append({
            'id': i.id,
            'content': i.content,
            'date': i.date,
            'user_id': i.user_id
        })

    return jsonify(response), 200
