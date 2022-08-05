from flask import Flask, render_template
from dotenv import load_dotenv
import os
from fake_posts import test_posts

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

@app.route("/books")
def get_books():
    books = test_posts['books']
    return render_template('books.html', books=books, title='Books')

@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = test_posts['thoughts']
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")

if __name__ == "__main__":
    app.run(debug=True)