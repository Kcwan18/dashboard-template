from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    aws_account_id = db.Column(db.String(100))
    url = db.Column(db.String(500))
    api_url = db.Column(db.String(500))
    score = db.Column(db.Integer, default=0)
    score_events = db.relationship('ScoreEvent', backref='user', lazy=True, cascade='all, delete-orphan')

class ScoreEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    reason = db.Column(db.String(200))
    points = db.Column(db.Integer)
