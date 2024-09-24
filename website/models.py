from .extentions import db
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    like = db.Column(db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=True)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Following(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    following = db.Column(db.String(100000))
    uploads = db.Column(db.String(100000))
    followers = db.Column(db.String(100000))
    likes = db.Column(db.String(100000))
    following_count = db.Column(db.Integer)
    uploads_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)

    def __init__(self, username):
        self.username = username
        self.following = '-1'
        self.followers = '-1'
        self.likes = '-1'
        self.followers_count = 0
        self.following_count = 0
        self.uploads_count = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_like(self, thought_id):
        self.likes += "/" + str(thought_id)
        db.session.commit()
        thought = Thought.query.filter_by(id=thought_id).first()
        thought.like += 1
        thought.save()

    def remove_like(self, thought_id):
        like_list = self.likes.split("/")
        like_list.remove(str(thought_id))
        self.likes = "/".join(like_list)
        db.session.commit()
        thought = Thought.query.filter_by(id=thought_id).first()
        thought.like -= 1
        thought.save()

    def get_likes(self):
        return self.likes.split("/")[1::]

    def add_following(self, username):
        self.following += "/" + str(username)
        self.following_count += 1
        db.session.commit()
        user_followed = Following.query.filter_by(username=username).first()
        user_followed.add_followers(self.username)

    def remove_following(self, username):
        following_list = self.following.split("/")
        following_list.remove(username)
        self.following_count -= 1
        self.following = "/".join(following_list)
        db.session.commit()
        user_followed = Following.query.filter_by(username=username).first()
        user_followed.remove_follower(self.username)

    def get_following(self):
        return self.following.split("/")[1::]

    def add_followers(self, username):
        self.followers += "/" + str(username)
        self.followers_count += 1
        db.session.commit()

    def remove_follower(self, username):
        follower_list = self.followers.split("/")
        follower_list.remove(username)
        print(follower_list)
        self.followers_count -= 1
        self.followers = "/".join(follower_list)
        db.session.commit()

    def get_followers(self):
        return self.followers.split("/")[1::]

    def add_thought(self):
        self.uploads_count += 1
 