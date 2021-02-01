from .app import main as main_blueprint
from flask import Flask

app = Flask(__name__)


def create_app():
    app.register_blueprint(main_blueprint)

    with app.app_context():
        return app