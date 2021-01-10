from datetime import datetime
from flask import render_template, flash, request, url_for, redirect
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm, SignupForm, CreateWorkspaceForm, TaskForm
from account import get_user, User
from flask_login import login_user, login_required, current_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from workspaceModel import Workspace

import dbop

auth = HTTPBasicAuth()

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        result, user = dbop.checkUserMail(email)
        if result:
            flash("Invalid email.", "email")
        else:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash("Invalid password", "password")
    return render_template("login.html", form=form)

def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.data["email"]
        name = form.data["name"]
        surname = form.data["surname"]
        password = form.data["password"]
        repeatpassword = form.data["repeatpassword"]
        result, user = dbop.checkUserMail(email)
        if result:
            if len(password) >= 6:
                if password == repeatpassword:
                    message, uid = dbop.registerUser(name, surname,email, hasher.hash(password))
                    if uid != -1:
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
                flash("Password must be at least 6 character!", "password")
        else:
            flash("This email is already used!", "email")
    return render_template("signup.html", form=form)

@login_required
def home_page():
    form = CreateWorkspaceForm()    
    if form.validate_on_submit():
        title = form.data["title"]
        description = form.data["description"]
        color = form.data["color"]
        order = form.data["order"]
        dbop.createWorkspace(title, description, color, order)
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(url_for("home_page"))
    wsArr = dbop.getUserWorkspaces(current_user.uid)
    wsData = []
    if(type(wsArr) != tuple):
        for i in wsArr:
            data = dbop.getWorkspaceData(i[2])
            if (type(data) != tuple):
                wsData.append(data)
    return render_template("home.html", user = current_user, form = form, data = wsData)

@login_required
def workspace_page():
    wid = request.args.get('wsId')
    data = Workspace(wid, request.args.get('title').replace("+", " "))
    wslists = dbop.getWsLists(wid)
    data.wslists = list(wslists)
    print(data.wslists)
    for i in range(len(data.wslists)):
        data.wslists[i] = list(data.wslists[i])
        tasks = dbop.getListTasks(data.wslists[i][0])
        if not (len(tasks) == 2 and tasks[1] == -1) and len(tasks) != 0 :
            for j in range(len(tasks)):
                tasks[j] = list(tasks[j])
                comments = dbop.getTaskComments(tasks[j][0])
                if not (len(comments) == 2 and comments[1] == -1) :
                    tasks[j].append(list(comments))
            data.wslists[i].append(list(tasks))
    taskForm = TaskForm()
    users = dbop.getWorkspaceUsers(wid)
    ws = dbop.getWorkspaceData(wid)
    print('data',data.wslists)
    return render_template("workspace.html", data = data.wslists, ws = ws[0], taskForm = taskForm, users = users)

@login_required
def statistics_page():
    return render_template("statistics.html")