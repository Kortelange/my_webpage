from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

@app.route("/books")
def get_books():
    return "Welcome to the books page!"

@app.route("/quick_thoughts")
def get_quick_thoughts():
    return render_template("quick_thoughts.html")

if __name__ == "__main__":
    app.run(debug=True)