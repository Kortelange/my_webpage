from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", fa_kit=os.environ.get("FA_KIT"))

if __name__ == "__main__":
    app.run(debug=True)