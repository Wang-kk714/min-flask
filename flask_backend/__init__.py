from flask import Flask
from . import views


def get_app():
    # create and configure the app
    app = Flask(__name__)

    app.add_url_rule('/', view_func=views.hello)
    return app
