from dotenv import load_dotenv
from flask import Flask

from .youtube_retrieval import yt_bp

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(yt_bp)

    return app
