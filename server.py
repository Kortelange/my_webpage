from flask import Flask, render_template
from dotenv import load_dotenv
import os
from fake_posts import test_posts
from flask_sqlalchemy import SQLAlchemy
import sqlite3

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_webpage.db"
db = SQLAlchemy(app)

class QuickThought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()


# populate database
# for thought in test_posts['thoughts']:
#    db.session.add(
#        QuickThought(title=thought['title'], content=thought['thought'])
#    )
#    db.session.commit()


def get_book_from_id(id):
    for book in test_posts['books']:
        if book['id'] == id:
            return book

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

@app.route("/books")
def get_books():
    books = test_posts['books']
    return render_template('books.html', books=books, title='Books')


@app.route("/books/<int:id>")
def get_book(id):
    book = get_book_from_id(id)
    return render_template('book.html', book=book, title=book['title'])


@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = QuickThought.query.all()
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")


if __name__ == "__main__":
    app.run(debug=True)