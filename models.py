from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class QuickThought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    short_review = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
