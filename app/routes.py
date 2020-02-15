from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Karan"}
    return render_template("index.html", user = user)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, rememberMe = {}".format(form.username.data, form.rememberMe.data))
        return redirect(url_for("index"))
    return render_template("login.html", title = "Login", form = form)