from flask import Blueprint, request, jsonify
from .models import Thought, Following
from flask_jwt_extended import jwt_required, current_user

api_social = Blueprint('api_social', __name__)


@api_social.route('/follow', methods=['POST'])
@jwt_required()
def follow():
    following = Following.query.filter_by(username=current_user.username).first()
    following.add_following(request.headers['username'])

    follower = Following.query.filter_by(username=request.headers['username']).first()
    follower.add_followers(current_user.username)

    follower.save()
    following.save()

    return jsonify({'message': 'Followed successfully'}), 202


@api_social.route('/unfollow', methods=['POST'])
@jwt_required()
def unfollow():
    following = Following.query.filter_by(username=current_user.username).first()
    following.remove_following(request.headers['username'])

    follower = Following.query.filter_by(username=request.headers['username']).first()
    follower.remove_followers(current_user.username)

    follower.save()
    following.save()

    return jsonify({'message': 'Unfollowed successfully'}), 202
