from flask_login import UserMixin
from .extentions import db


class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)


class Following(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    following = db.Column(db.String(100000))
    uploads = db.Column(db.String(100000))
    followers = db.Column(db.String(100000))
    following_count = db.Column(db.Integer)
    uploads_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)

    def __init__(self, username):
        self.username = username
        self.following = '-1'
        self.followers = '-1'
        self.uploads = '-1'
        self.followers_count = 0
        self.following_count = 0
        self.uploads_count = 0

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

    def add_image(self, name):
        self.uploads += "/" + str(name)
        self.uploads_count += 1
        db.session.commit()

    def get_images(self):
        return self.uploads.split("/")[1::]
 