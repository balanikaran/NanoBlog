from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Karan"}
    return render_template("index.html", title = "Karan's", user = user)