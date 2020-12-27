from datetime import datetime
from flask import render_template, flash, request, url_for, redirect
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm, SignupForm
from account import get_user
from flask_login import login_user, login_required, current_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import dbop


auth = HTTPBasicAuth()

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        user = get_user(email)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash("Invalid password", "password")
        else:
            flash("Invalid email.", "email")
    return render_template("login.html", form=form)

def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.data["email"]
        name = form.data["name"]
        surname = form.data["surname"]
        password = form.data["password"]
        passwordAgain = form.data["passwordAgain"]
        result = dbop.checkUserMail(email)
        if result:
            if password == passwordAgain:
                if dbop.registerUser(name, surname,email, password) != 0:
                    login_user(user)
                    flash("You have logged in.")
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
                else:
                    flash("insert error", "passwordAgain")
            else:
                flash("Password must match!", "passwordAgain")
        else:
            flash("Invalid email.", "email")
    return render_template("signup.html", form=form)

@login_required
def home_page():
    return render_template("home.html")

@login_required
def workspace_page():
    return render_template("workspace.html")

@login_required
def statistics_page():
    return render_template("statistics.html")