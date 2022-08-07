from flask import Flask, render_template, redirect
from dotenv import load_dotenv
import os
from fake_posts import test_posts
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
from models import QuickThought, Book, db
from forms import QuickThoughtForm, BookForm


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_webpage.db"
app.secret_key = "very secret"
ckeditor = CKEditor(app)
db.init_app(app)
# db.create_all()



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


@app.route("/books/new", methods=["GET", "POST"])
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        print("heloo im here!")
        book = Book(
                title=form.title.data,
                author=form.author.data,
                short_review=form.short_review.data,
                body=form.body.data,
                rating=form.rating.data
            )
        db.session.add(
            book
        )
        db.session.commit()
        return redirect(f"/books/{book.id}")
    return render_template('new_book.html', title='New Book', form=form)


@app.route("/books/delete/<int:id>")
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/books")



@app.route("/books/<int:id>")
def get_book(id):
    book = Book.query.get(id)
    return render_template('book.html', book=book, title=book.title)


@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = QuickThought.query.all()
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")


@app.route("/quick_thoughts/delete/<int:id>")
def delete_quick_thought(id):
    thought = QuickThought.query.get(id)
    db.session.delete(thought)
    db.session.commit()
    return redirect("/quick_thoughts")


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