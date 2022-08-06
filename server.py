from flask import Flask, render_template, redirect
from dotenv import load_dotenv
import os
from fake_posts import test_posts
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_webpage.db"

app.secret_key = "very secret"
db = SQLAlchemy(app)

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


db.create_all()


# populate database
# for thought in test_posts['thoughts']:
#    db.session.add(
#        QuickThought(title=thought['title'], content=thought['thought'])
#    )
#    db.session.commit()
# for book in test_posts['books']:
#     db.session.add(
#         Book(
#             title=book['title'],
#             author=book['author'],
#             short_review=book['short_review'],
#             body=book['long_review'],
#             rating=book['rating']
#         )
#     )
#     db.session.commit()


class QuickThoughtForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    submit = SubmitField(label="Add thought")

# class BookForm(FlaskForm):
#     title = StringField('title', )


def get_book_from_id(id):
    for book in test_posts['books']:
        if book['id'] == id:
            return book

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

@app.route("/books")
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books, title='Books')


@app.route("/books/<int:id>")
def get_book(id):
    book = get_book_from_id(id)
    return render_template('book.html', book=book, title=book['title'])


@app.route("/books/new")
def new_book():
    return render_template('new_book.html', title='New Book')


@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = QuickThought.query.all()
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")


@app.route("/quick_thoughts/new", methods=["GET", "POST"])
def new_quick_thought():
    form = QuickThoughtForm()
    if form.validate_on_submit():
        db.session.add(
            QuickThought(
                title=form.title.data,
                content=form.content.data
            )
        )
        db.session.commit()
        return redirect("/quick_thoughts")
    return render_template("new_quick_thought.html", form=form, title="New Thought")


if __name__ == "__main__":
    app.run(debug=True)