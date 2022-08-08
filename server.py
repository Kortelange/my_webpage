from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from flask_ckeditor import CKEditor, CKEditorField
from models import QuickThought, Book, db, User
from forms import QuickThoughtForm, BookForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required
from datetime import date


load_dotenv()

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(uri,  "sqlite:///my_webpage.db")
app.secret_key = os.environ.get("APP_SECRET_KEY")
ckeditor = CKEditor(app)
db.init_app(app)
app.app_context().push()
# db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(1)
        if check_password_hash(user.password, form.password.data):
            login_user(user)
        return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/books")
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books, title='Books')


@app.route("/books/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        print("Hello")
        book = Book(
                title=form.title.data,
                author=form.author.data,
                short_review=form.short_review.data,
                body=form.body.data,
                rating=form.rating.data,
                add_date=date.today(),
                upd_date=date.today()
            )
        db.session.add(
            book
        )
        db.session.commit()
        return redirect(f"/books/{book.id}")

    return render_template(
        'new_book.html',
        title='New Book',
        form=form,
        action="/books/new"
    )


@app.route("/books/delete/<int:id>")
@login_required
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/books")


@app.route("/books/<int:id>")
def get_book(id):
    book = Book.query.get(id)
    return render_template('book.html', book=book, title=book.title)


@app.route("/books/<int:id>/edit", methods=["GET","POST"])
@login_required
def edit_book(id):
    book = Book.query.get(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        book.upd_date = date.today()
        db.session.commit()
        return redirect(f"/books/{book.id}")

    form.submit.label.text = "Update"
    return render_template(
        'new_book.html',
        form=form,
        title=f'Edit {book.title}',
        action=f'/books/{book.id}/edit'
    )


@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = QuickThought.query.all()
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")


@app.route("/quick_thoughts/new", methods=["GET", "POST"])
@login_required
def new_quick_thought():
    form = QuickThoughtForm()
    if form.validate_on_submit():
        db.session.add(
            QuickThought(
                title=form.title.data,
                content=form.content.data,
                add_date=date.today(),
                upd_date=date.today()
            )
        )
        db.session.commit()
        return redirect("/quick_thoughts")

    return render_template(
        "new_quick_thought.html",
        form=form,
        title="New Thought",
        action="/quick_thoughts/new"
    )


@app.route("/quick_thoughts/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_quick_thought(id):
    thought = QuickThought.query.get(id)
    form = QuickThoughtForm(obj=thought)
    if form.validate_on_submit():
        form.populate_obj(thought)
        thought.upd_date = date.today()
        db.session.commit()
        return redirect("/quick_thoughts")

    form.submit.label.text = "Update"
    return render_template(
        "new_quick_thought.html",
        form=form,
        title=f"Edit {thought.title}",
        action=f"/quick_thoughts/{thought.id}/edit"
    )


@app.route("/quick_thoughts/delete/<int:id>")
@login_required
def delete_quick_thought(id):
    thought = QuickThought.query.get(id)
    db.session.delete(thought)
    db.session.commit()
    return redirect("/quick_thoughts")


if __name__ == "__main__":
    app.run()
