from app import db, login
from flask_login import UserMixin
from flask import current_app
from datetime import datetime, timedelta
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(140), nullable=True)

    communities = db.relationship('Community', secondary='community_members')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_password_reset_token(self, expires_in=600):
        return jwt.encode(
            {'password_reset': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['password_reset']
        except Exception:
            return None
        return User.query.get(id)


class Community(db.Model):
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), unique=True, index=True)
    about = db.Column(db.String(128))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_by_user = db.relationship('User')

    def __repr__(self):
        return f'<Community {self.name}>'


class Messages(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender_type = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"))

    def __repr__(self):
        return f'<Messages {self.content}>'


community_members = db.Table(
    'community_members',
    db.Column('community_id', db.Integer, db.ForeignKey("communities.id")),
    db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
    db.Column('joined_date', db.DateTime, default=db.func.current_timestamp())
)