from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_login import LoginManager
import views
import os
from account import get_user

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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

    lm.init_app(app)
    lm.login_view = "login_page"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
