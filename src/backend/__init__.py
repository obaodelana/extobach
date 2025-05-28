from dotenv import load_dotenv
from flask import Flask

from .retrieval.routes import retrieval_bp
from .sonar.routes import sonar_bp
from .stats.routes import stats_bp

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(retrieval_bp)
    app.register_blueprint(sonar_bp)
    app.register_blueprint(stats_bp)

    return app
