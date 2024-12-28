
from datetime import datetime
from db.setup_db import db

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class QuizHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    score = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.JSON, nullable=False)  # Store answers as JSON
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

# Helper functions for pagination
def paginate_query(query, page, per_page):
    return query.paginate(page=page, per_page=per_page, error_out=False)
