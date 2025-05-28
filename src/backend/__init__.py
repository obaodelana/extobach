from dotenv import load_dotenv
from flask import Flask

from .retrieval.routes import retrieval_bp

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(retrieval_bp)

    return app
