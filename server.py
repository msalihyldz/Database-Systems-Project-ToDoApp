from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required
import views
import os
from account import get_user
import json
import dbop
import forms

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    if type(user_id) is not int and user_id[1] == -1:
        return None
    else:
        return get_user(user_id)


app = Flask(__name__)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if(request.method == 'GET'):
        return json.dumps(dbop.getUsers())

@app.route('/log_out', methods=['GET'])
def log_out():
    logout_user()
    flash("log out user...")
    return jsonify("Ok")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/addTask', methods=['POST'])
def addTask():
    content = request.form["content"]
    listId = request.form["listId"]
    assignedId = request.form["assignedId"]
    endDate = request.form["endDate"]
    importance = request.form["importance"]
    listorder = request.form["listorder"]
    result = dbop.addTask(content, listId, assignedId, endDate, importance, listorder)
    if type(result) is tuple:
        return "result[0]"
    else:
        return "Ok"

@app.route('/editTask', methods=['POST'])
def editTask():
    jsonData = request.get_json()
    tId = jsonData["taskId"]
    content = jsonData["content"]
    listId = jsonData["listId"]
    assignedId = jsonData["assignedId"]
    endDate = jsonData["endDate"]
    isDone = jsonData["isDone"]
    importance = jsonData["importance"]
    listorder = jsonData["listorder"]
    print(jsonData)
    result = dbop.updateTask(tId, content, listId, assignedId, endDate, isDone, importance, listorder)
    if(type(result) == tuple):
        return jsonify(result = "error")
    else:
        return jsonify(result = result)
    
@app.route('/addList', methods=['POST'])
def addList():
    title = request.form["title"]
    wid = request.form["wid"]
    result = dbop.addList(title, wid)
    if type(result) is tuple:
        return "result[0]"
    else:
        return "Ok" 

@app.route('/addFriend', methods=['POST'])
def addFriend():
    email = request.form["email"]
    wid = request.form["wid"]
    result, user = dbop.checkUserMail(email)
    if type(result) is tuple:
        return "error"
    else:
        if result == False:
            dbop.addFriend(user.uid, wid)
            return "Ok"
        else:
            return "Not Found"

@app.route('/addComment', methods=['POST'])
def addComment():
    taskId = request.form["taskId"]
    content = request.form["content"]
    result = dbop.addComment(content, taskId)
    if type(result) is tuple:
        return "error"
    else:
        return "Ok"

@app.route('/deleteTask', methods=['POST'])
def deleteTask():
    taskId = request.form["taskId"]
    result = dbop.deleteTask(taskId)
    if type(result) is tuple:
        return "error"
    else:
        return "Ok"

@app.route('/editWorkspace', methods=['POST'])
def editWorkspace():
    jsonData = request.get_json()
    wsId = jsonData["wsId"]
    title = jsonData["title"]
    description = jsonData["description"]
    color = jsonData["color"]
    order = jsonData["order"]
    result = dbop.updateWorkspace(wsId, title, description, color, order)
    if(type(result) == tuple):
        return jsonify(result = "error")
    else:
        return jsonify(result = result)

@app.route('/deleteWorkspace', methods=['POST'])
def deleteWorkspace():
    wsId = request.form["wsId"]
    result = dbop.deleteWorkspace(wsId)
    if type(result) is tuple:
        return "error"
    else:
        return "Ok"
    
@app.route('/editUser', methods=['POST'])
def editUser():
    jsonData = request.get_json()
    uId = jsonData["uId"]
    name = jsonData["name"]
    surname = jsonData["surname"]
    result = dbop.updateUser(uId, name, surname)
    if(type(result) == tuple):
        return jsonify(result = "error")
    else:
        return jsonify(result = result)

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    result = dbop.deleteUser()
    if(type(result) == tuple):
        return jsonify(result = "error")
    else:
        log_out()
        print(result)
        return jsonify(result = "Ok")

def page_not_found(e):
  return render_template('page404.html'), 404

def create_app():
    app.config.from_object("settings")
    app.add_url_rule(
        "/", view_func=views.home_page, methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/signup", view_func=views.signup_page, methods=["GET", "POST"]
    )

    
    app.add_url_rule(
        "/profile", view_func=views.profile_page, methods=["GET", "POST"]
    )

    app.add_url_rule("/workspace", view_func=views.workspace_page)
    app.add_url_rule("/statistics", view_func=views.statistics_page)
    app.add_url_rule("/login", view_func=views.login_page)

    app.register_error_handler(404, page_not_found)

    return app



lm.init_app(app)
lm.login_view = "login_page"

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
