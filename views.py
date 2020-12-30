from datetime import datetime
from flask import render_template, flash, request, url_for, redirect
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm, SignupForm
from account import get_user, User
from flask_login import login_user, login_required, current_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import dbop

auth = HTTPBasicAuth()

def login_page():
    print("login")
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        result, user = dbop.checkUserMail(email)
        if result:
            flash("Invalid email.", "email")
        else:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                print(user)
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash("Invalid password", "password")
    return render_template("login.html", form=form)

def signup_page():
    form = SignupForm()
    print(form.data)
    if form.validate_on_submit():
        email = form.data["email"]
        name = form.data["name"]
        surname = form.data["surname"]
        password = form.data["password"]
        repeatpassword = form.data["repeatpassword"]
        result, user = dbop.checkUserMail(email)
        if result:
            if password == repeatpassword:
                message, uid = dbop.registerUser(name, surname,email, hasher.hash(password))
                if uid is not -1:
                    user = User(uid, email, password, name, surname)
                    login_user(user)
                    flash("You have logged in.")
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
                else:
                    flash("insert error", "repeatpassword")
            else:
                flash("Password must match!", "repeatpassword")
        else:
            flash("This email is already used!", "email")
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