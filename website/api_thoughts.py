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
    page = request.args.get('page', 1, type=int)

    thoughts = Thought.query.order_by(Thought.date.desc()).paginate(page=page, per_page=10, error_out=False).items

    response = []

    for i in thoughts:
        response.append({
            'id': i.id,
            'content': i.content,
            'date': i.date,
            'user_id': i.user_id,
            'likes': i.like,
            'liked': False
        })

    return jsonify(response), 200


@api_thoughts.route('/get-with-login')
@jwt_required()
def get_with_login():
    page = request.args.get('page', 1, type=int)

    thoughts = Thought.query.order_by(Thought.date.desc()).paginate(page=page, per_page=10, error_out=False).items

    response = []

    current_user_likes = Following.query.filter_by(username=current_user.username).first().get_likes()

    for i in thoughts:
        response.append({
            'id': i.id,
            'content': i.content,
            'date': i.date,
            'user_id': i.user_id,
            'likes': i.like,
            'liked': True if current_user and str(i.id) in current_user_likes else False
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


@api_thoughts.post('/like')
@jwt_required()
def like_thought():
    data = request.get_json()
    thought_id = data.get('thought_id')

    thought = Thought.query.filter_by(id=thought_id).first()

    if not thought:
        return jsonify({'message': 'Thought not found'}), 404

    following = Following.query.filter_by(username=current_user.username).first()

    if str(thought_id) in following.get_likes():
        following.remove_like(thought_id)
        thought.like -= 1
    else:
        following.add_like(thought_id)
        thought.like += 1

    following.save()
    thought.save()

    return jsonify({'message': 'Success'}), 200
