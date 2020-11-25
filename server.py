from flask import Flask, request, jsonify, render_template

import views


app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)




def create_app():
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/workspace", view_func=views.workspace_page)
    app.add_url_rule("/statistics", view_func=views.statistics_page)
    app.add_url_rule("/login", view_func=views.login_page)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)