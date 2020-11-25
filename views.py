from datetime import datetime

from flask import render_template


def login_page():
    return render_template("login.html")

def home_page():
    return render_template("home.html")

def workspace_page():
    return render_template("workspace.html")

def statistics_page():
    return render_template("statistics.html")