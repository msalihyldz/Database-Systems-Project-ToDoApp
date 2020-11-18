from datetime import datetime

from flask import render_template


def home_page():
    return render_template("home.html")


def workspace_page():
    return render_template("workspace.html")