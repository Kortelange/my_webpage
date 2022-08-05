from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

posts_link = "https://api.npoint.io/04e651e9ca9922d160cd"

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

@app.route("/books")
def get_books():
    books = requests.get(posts_link).json()['books']
    return render_template('books.html', books=books, title='Books')

@app.route("/quick_thoughts")
def get_quick_thoughts():
    thoughts = requests.get(posts_link).json()['thoughts']
    return render_template("quick_thoughts.html", thoughts=thoughts, title="Quick Thoughts")

if __name__ == "__main__":
    app.run(debug=True)