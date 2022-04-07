from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .test import test
    from .views import views
    app.register_blueprint(test, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
