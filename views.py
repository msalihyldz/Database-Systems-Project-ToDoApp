from datetime import datetime
from flask import render_template, flash, request, url_for, redirect
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm
from account import get_user
from flask_login import login_user


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

def home_page():
    return render_template("home.html")

def workspace_page():
    return render_template("workspace.html")

def statistics_page():
    return render_template("statistics.html")