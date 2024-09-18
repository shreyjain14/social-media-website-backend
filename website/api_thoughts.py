from datetime import datetime
from flask import Blueprint, request, jsonify
from .extentions import db
from .models import Thought
from flask_jwt_extended import jwt_required, current_user

api_thoughts = Blueprint('api_thoughts', __name__)


@api_thoughts.route('/create', methods=['POST'])
@jwt_required()
def create():
    content = request.headers['content']

    if request.headers['anonymous'] == 'true':
        thought = Thought(content=content, date=datetime.now())
    else:
        thought = Thought(content=content, date=datetime.now(), user_id=current_user.username)
    db.session.add(thought)
    db.session.commit()

    return jsonify({'message': 'Thought created successfully'}), 201


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

    return response
