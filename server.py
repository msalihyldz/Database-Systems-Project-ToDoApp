from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, flash
from flask_login import LoginManager, logout_user
import views
import os
from account import get_user
import json
import dbop

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
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

def page_not_found(e):
  return render_template('page404.html'), 404

def create_app():
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)

    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/signup", view_func=views.signup_page, methods=["GET", "POST"]
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
