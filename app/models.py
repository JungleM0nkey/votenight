from app import db, login
from datetime import datetime
from pytz import timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

tz = timezone('EST')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer)
    last_vote = db.Column(db.String(80))

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_points(self):
        return self.points

    def remove_point(self):
        self.points = self.points - 1

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(80))
    username = db.Column(db.String(16), index=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    votes = db.Column(db.Integer)
    poster = db.Column(db.String(256))
    year = db.Column(db.Integer)
    rating = db.Column(db.String(12))
    plot = db.Column(db.String)
    genres = db.Column(db.String)
    category = db.Column(db.String(32))
    director = db.Column(db.String)
    imdb_page = db.Column(db.String)

    def __repr__(self):
        return f"<Movies(movie={self.movie}, username={self.username}, date={self.date}, votes={self.votes})>"

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True)
    username = username = db.Column(db.String(16))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return self.code

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(80))
    username = db.Column(db.String(16), index=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    category = db.Column(db.String)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))